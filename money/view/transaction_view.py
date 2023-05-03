from collections import defaultdict
from typing import Any, Dict

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Min, Prefetch, QuerySet, Sum
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView

from money import forms as money_forms
from money import helper, models


# Transaction related views
class TransactionListView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "transaction/transaction_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["usd_data"] = helper.get_transaction_chart_data(
            models.Transaction.objects.filter(
                account__currency=models.CurrencyType.USD
            ).order_by("date", "-amount"),
            recalculate=True,
        )

        context["krw_data"] = helper.get_transaction_chart_data(
            models.Transaction.objects.filter(
                account__currency=models.CurrencyType.KRW
            ).order_by("date", "-amount"),
            recalculate=True,
        )

        return context


transaction_list_view = TransactionListView.as_view()


class TransactionCreateView(LoginRequiredMixin, CreateView):
    template_name = "transaction/transaction_create.html"
    model = models.Transaction
    form_class = money_forms.TransactionForm

    def get_success_url(self) -> str:
        return reverse_lazy(
            "money:transaction_create", kwargs={"account_id": self.kwargs["account_id"]}
        )

    def get_form(self) -> forms.BaseModelForm:
        form = super().get_form()
        form.initial["account"] = self.kwargs["account_id"]
        date_default = self.request.GET.get("date", None)
        if date_default:
            form.initial["date"] = date_default

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = models.Transaction.objects.filter(
            account_id=self.kwargs["account_id"]
        ).order_by("-date", "amount")

        if len(transaction) > 0:
            latest_transaction = transaction[0]
        else:
            latest_transaction = None

        if latest_transaction:
            context["form"].initial["date"] = latest_transaction.date.strftime(
                "%Y-%m-%d"
            )

        context["latest_transaction"] = latest_transaction
        context["account"] = models.Account.objects.get(pk=self.kwargs["account_id"])
        return context


transaction_create_view = TransactionCreateView.as_view()


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = models.Transaction
    template_name = "transaction/transaction_detail.html"

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .select_related(
                "account",
                "related_transaction",
                "related_transaction__retailer",
                "retailer",
            )
            .prefetch_related(
                Prefetch(
                    "transactiondetail_set",
                    queryset=models.TransactionDetail.objects.all().select_related(
                        "item"
                    ),
                )
            )
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        transaction = context["transaction"]
        detail_sum = 0

        for detail in transaction.transactiondetail_set.all():
            detail_sum += detail.amount * detail.count
        context["detail_sum"] = detail_sum

        if abs(transaction.amount + detail_sum) < 0.01:
            transaction.reviewed = True
            transaction.save()

        return context


transaction_detail_view = TransactionDetailView.as_view()


class TransactionDetailCreateView(LoginRequiredMixin, CreateView):
    template_name = "transaction/transaction_detail_create.html"
    model = models.TransactionDetail
    form_class = money_forms.TransactionDetailForm

    def get_success_url(self) -> str:
        return reverse_lazy(
            "money:transaction_detail_create",
            kwargs={"transaction_id": self.kwargs["transaction_id"]},
        )

    def form_valid(self, form: forms.BaseModelForm) -> HttpResponse:
        form.instance.transaction = models.Transaction.objects.get(
            pk=self.kwargs["transaction_id"]
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        transaction = models.Transaction.objects.select_related(
            "account", "retailer"
        ).get(pk=self.kwargs["transaction_id"])
        context["transaction"] = transaction

        leftover = -transaction.amount

        details = transaction.transactiondetail_set.all().select_related("item")

        for detail in details:
            leftover -= detail.count * detail.amount

        context["details"] = details
        context["leftover"] = leftover
        return context


transaction_detail_create_view = TransactionDetailCreateView.as_view()


# Transaction category related views
class TransactionCategoryView(LoginRequiredMixin, View):
    template_name = "dashboard/category.html"

    def get(self, request, *args, **kwargs):
        selected_month = request.GET.get("month")

        query = models.Transaction.objects.values("type", "account__currency")

        context = {}

        if selected_month:
            selected_month_split = selected_month.split("-")
            context["selected_month"] = (
                selected_month,
                f"{selected_month_split[0]}년 {selected_month_split[1]}월",
            )
            query = query.filter(date__year=selected_month_split[0]).filter(
                date__month=selected_month_split[1]
            )

        context["summarization"] = query.annotate(total_amount=-Sum("amount")).order_by(
            "account__currency", "-total_amount"
        )

        label_per_currency = {k[0]: [] for k in models.CurrencyType.choices}
        data_per_currency = {k[0]: [] for k in models.CurrencyType.choices}
        income_per_currency = {k[0]: [] for k in models.CurrencyType.choices}
        spent_per_currency = {k[0]: [] for k in models.CurrencyType.choices}

        for summary in context["summarization"]:
            if summary["total_amount"] > 0:
                label_per_currency[summary["account__currency"]].append(summary["type"])
                data_per_currency[summary["account__currency"]].append(
                    summary["total_amount"]
                )
                spent_per_currency[summary["account__currency"]].append(summary)
            else:
                income_per_currency[summary["account__currency"]].append(summary)

        context["label"] = label_per_currency
        context["data"] = data_per_currency
        context["income"] = sorted([(k, v) for k, v in income_per_currency.items()])
        context["spent"] = sorted([(k, v) for k, v in spent_per_currency.items()])

        date_range = models.Transaction.objects.aggregate(Min("date"), Max("date"))
        context["months"] = helper.get_month_list(
            date_range["date__min"], date_range["date__max"]
        )
        context["currencies"] = [k[0] for k in models.CurrencyType.choices]

        return render(request, self.template_name, context)


transaction_category_view = TransactionCategoryView.as_view()


# Transaction review related views
class ReviewTransactionView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "review/review_transaction.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs.filter(reviewed=False)
            .order_by("date", "amount")
            .prefetch_related("account")
        )
        return qs


review_transaction_view = ReviewTransactionView.as_view()


class ReviewInternalTransactionView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "review/review_internal.html"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()

        qs = (
            qs.filter(reviewed=False)
            .filter(type=models.TransactionCategory.TRANSFER)
            .order_by("date", "amount")
            .prefetch_related("account")
        )

        if self.request.GET.get("internal_only", False):
            qs = qs.filter(is_internal=True)

        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("internal_only", False):
            context["internal_only"] = True

        return context


review_internal_transaction_view = ReviewInternalTransactionView.as_view()


class ReviewDetailTransactionView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "review/review_detail.html"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .filter(requires_detail=True)
            .filter(reviewed=False)
            .prefetch_related("retailer")
            .order_by("-date")
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


review_detail_transaction_view = ReviewDetailTransactionView.as_view()


class StockTransactionCreateView(LoginRequiredMixin, CreateView):
    template_name = "stock/stock_transaction_create.html"
    model = models.StockTransaction
    form_class = money_forms.StockTransactionForm

    def get_success_url(self) -> str:
        return reverse_lazy(
            "money:stock_transaction_create",
            kwargs={"account_id": self.kwargs["account_id"]},
        )

    def get_form(self) -> forms.BaseModelForm:
        form = super().get_form()
        form.initial["account"] = self.kwargs["account_id"]

        date_default = self.request.GET.get("date", None)
        if date_default:
            form.initial["date"] = date_default

        return form

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        account_id = self.kwargs["account_id"]

        return super().get_context_data(**kwargs)


stock_transaction_create_view = StockTransactionCreateView.as_view()


class StockTransactionView(LoginRequiredMixin, DetailView):
    template_name = "stock/stock_transaction_detail.html"
    model = models.StockTransaction


stock_transaction_detail_view = StockTransactionView.as_view()


class AmazonListView(LoginRequiredMixin, ListView):
    template_name = "transaction/amazon_list.html"
    model = models.Transaction

    def get_queryset(self) -> QuerySet[Any]:
        amazon = models.Retailer.objects.filter(name="Amazon")
        if amazon:
            return (
                super()
                .get_queryset()
                .filter(retailer=amazon[0])
                .prefetch_related("account")
            ).order_by("-date")
        else:
            return None


amazon_list_view = AmazonListView.as_view()
