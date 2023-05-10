from typing import Any, Dict

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Min, Prefetch, QuerySet, Sum, Count
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, View
from django.views.generic.edit import CreateView

from money import forms as money_forms
from money import helper, models


# Transaction related views
class TransactionListView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "transaction/transaction_list.html"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().order_by("-date")
        qs = helper.filter_month(self.request, qs)

        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        date_range = models.Transaction.objects.aggregate(Min("date"), Max("date"))
        helper.update_month_info(
            self.request,
            context,
            date_range["date__min"],
            date_range["date__max"],
        )

        return context


transaction_list_view = TransactionListView.as_view()


class TransactionChartListView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "transaction/transaction_chart_list.html"

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


transaction_chart_list_view = TransactionChartListView.as_view()


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
        ).order_by("-date", "amount", "balance")

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


class TransactionUpdateView(UpdateView):
    template_name = "transaction/transaction_update.html"
    model = models.Transaction
    form_class = money_forms.TransactionUpdateForm


transaction_update_view = TransactionUpdateView.as_view()


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
        if form.cleaned_data["amount"] == 0:
            form.add_error("amount", "Value must not be 0.")
            return self.form_invalid(form)

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
        query_set = models.Transaction.objects.values("type", "account__currency")
        query_set = helper.filter_month(request, query_set)

        context = {}

        date_range = models.Transaction.objects.aggregate(Min("date"), Max("date"))
        helper.update_month_info(
            request,
            context,
            date_range["date__min"],
            date_range["date__max"],
        )

        context["summarization"] = query_set.annotate(
            total_amount=-Sum("amount")
        ).order_by("account__currency", "-total_amount")

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
            .order_by("-date", "amount")
            .prefetch_related("account", "retailer")
        )
        return qs


review_transaction_view = ReviewTransactionView.as_view()


class ReviewInternalTransactionView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "review/review_internal.html"
    paginate_by = 20

    INTERNAL_ONLY_FLAG = "internal_only"

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()

        qs = (
            qs.filter(reviewed=False)
            .filter(type=models.TransactionCategory.TRANSFER)
            .order_by("-date", "amount")
            .prefetch_related("account", "retailer", "related_transaction")
        )

        if self.request.GET.get(self.INTERNAL_ONLY_FLAG, False):
            qs = qs.filter(is_internal=True)

        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.GET.get(self.INTERNAL_ONLY_FLAG, False):
            context["additional_get_query"] = f"&{self.INTERNAL_ONLY_FLAG}=True"

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
            .prefetch_related("account", "retailer")
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
                .order_by("-date")
                .annotate(order_count=Count("amazonorder"))
            )
        else:
            return None


amazon_list_view = AmazonListView.as_view()


class AmazonOrderListView(LoginRequiredMixin, ListView):
    template_name = "transaction/amazon_order_list.html"
    model = models.AmazonOrder

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super()
            .get_queryset()
            .order_by("date", "id")
            .prefetch_related(
                "transaction",
                Prefetch(
                    "transaction__account",
                    queryset=models.Account.objects.all(),
                ),
                Prefetch(
                    "transaction__retailer",
                    queryset=models.Retailer.objects.all(),
                ),
            )
        )


amazon_order_list_view = AmazonOrderListView.as_view()


class AmazonOrderCreateView(LoginRequiredMixin, CreateView):
    template_name = "transaction/amazon_create.html"
    model = models.AmazonOrder
    form_class = money_forms.AmazonOrderForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        prev_order = models.AmazonOrder.objects.last()

        if prev_order:
            context["form"].initial["date"] = prev_order.date

        context["prev_order"] = prev_order

        return context


amazon_order_create_view = AmazonOrderCreateView.as_view()


class AmazonOrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "transaction/amazon_order_detail.html"
    model = models.AmazonOrder


amazon_order_detail_view = AmazonOrderDetailView.as_view()
