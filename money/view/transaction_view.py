from datetime import date
from typing import Any, Dict

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import (
    Case,
    Count,
    FloatField,
    Max,
    Min,
    Prefetch,
    Q,
    QuerySet,
    Sum,
    When,
)
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, View
from django.views.generic.edit import CreateView

from money import choices
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

        reviewed = self.request.GET.get("reviewed", None)
        if reviewed is not None:
            qs = qs.filter(reviewed=reviewed)

        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        date_range = models.Transaction.objects.aggregate(Min("date"), Max("date"))
        context["additional_get_query"] = {}
        helper.update_month_info(
            self.request,
            context,
            date_range["date__min"],
            date_range["date__max"],
        )

        reviewed = self.request.GET.get("reviewed", None)
        if reviewed is not None:
            context["additional_get_query"]["reviewed"] = reviewed

        return context


transaction_list_view = TransactionListView.as_view()


class TransactionChartListView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "transaction/transaction_chart_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        amountsnapshot_list = models.AmountSnapshot.objects.all()
        context["chart"] = {
            "USD": helper.snapshot_chart(amountsnapshot_list, choices.CurrencyType.USD),
            "KRW": helper.snapshot_chart(amountsnapshot_list, choices.CurrencyType.KRW),
        }

        selected_year = self.request.GET.get("year", date.today().year)
        monthly_summary = (
            models.Transaction.objects.filter(is_internal=False)
            .filter(~Q(type=choices.TransactionCategory.STOCK))
            .annotate(month=TruncMonth("date"))
            .values("month", "account__currency")
            .annotate(
                total_amount=Sum("amount"),
                minus_sum=Sum(
                    Case(
                        When(amount__lt=0, then="amount"),
                        default=0,
                        output_field=FloatField(),
                    )
                ),
                plus_sum=Sum(
                    Case(
                        When(amount__gt=0, then="amount"),
                        default=0,
                        output_field=FloatField(),
                    )
                ),
            )
            .order_by("-month", "account__currency")
        )

        context["year_list"] = {summary["month"].year for summary in monthly_summary}

        if str(selected_year).lower() != "all":
            monthly_summary = monthly_summary.filter(month__year=selected_year)

        context["monthly_summary"] = monthly_summary
        context["selected_year"] = selected_year

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


# Transaction category related views
class TransactionCategoryView(LoginRequiredMixin, View):
    template_name = "category/category.html"

    def get(self, request, *args, **kwargs):
        query_set = models.Transaction.objects.values("type", "account__currency")
        query_set = helper.filter_month(request, query_set)

        context = {"additional_get_query": {}}

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
        context["income"] = sorted(income_per_currency.items())
        context["spent"] = sorted(spent_per_currency.items())
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["additional_get_query"] = {}
        return context


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

        qs = helper.filter_month(self.request, qs)

        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["additional_get_query"] = {}
        if self.request.GET.get(self.INTERNAL_ONLY_FLAG, False):
            context["additional_get_query"][self.INTERNAL_ONLY_FLAG] = True

        date_range = models.Transaction.objects.aggregate(Min("date"), Max("date"))
        helper.update_month_info(
            self.request,
            context,
            date_range["date__min"],
            date_range["date__max"],
        )
        return context


review_internal_transaction_view = ReviewInternalTransactionView.as_view()


class ReviewDetailTransactionView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "review/review_detail.html"
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        reviewed = self.request.GET.get("reviewed", False)
        return (
            super()
            .get_queryset()
            .filter(requires_detail=True)
            .filter(reviewed=reviewed)
            .prefetch_related("account", "retailer", "transactiondetail_set")
            .order_by("-date")
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["additional_get_query"] = {}
        context["reviewed"] = self.request.GET.get("reviewed", False)
        context["additional_get_query"]["reviewed"] = context["reviewed"]
        return context


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

    @transaction.atomic
    def form_valid(self, form):
        stock_transaction = form.save(commit=False)
        stock_transaction.amount = round(
            form.cleaned_data["price"] * form.cleaned_data["shares"], 2
        )

        # Create account transaction
        transaction = models.Transaction.objects.create(
            account=stock_transaction.account,
            amount=-stock_transaction.amount,
            date=stock_transaction.date,
            note=stock_transaction.note,
            type=choices.TransactionCategory.STOCK,
        )
        transaction.save()

        stock_transaction.related_transaction = transaction
        stock_transaction.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        account_id = self.kwargs["account_id"]
        context["account"] = models.Account.objects.get(pk=account_id)

        return context


stock_transaction_create_view = StockTransactionCreateView.as_view()


class StockTransactionView(LoginRequiredMixin, DetailView):
    template_name = "stock/stock_transaction_detail.html"
    model = models.StockTransaction


stock_transaction_detail_view = StockTransactionView.as_view()


class AmazonListView(LoginRequiredMixin, ListView):
    template_name = "transaction/amazon_list.html"
    model = models.Transaction
    paginate_by = 20

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["additional_get_query"] = {}

        return context

    def get_queryset(self) -> QuerySet[Any]:
        amazon = models.Retailer.objects.filter(name="Amazon")
        if amazon:
            return (
                super()
                .get_queryset()
                .filter(retailer=amazon[0])
                .annotate(
                    num_amazon_order=Count("amazonorder"),
                    num_return_order=Count("returned_order"),
                )
                .filter(num_amazon_order=0, num_return_order=0)
                .prefetch_related("account")
                .order_by("-date")
            )
        else:
            return None


amazon_list_view = AmazonListView.as_view()


class AmazonOrderListView(LoginRequiredMixin, ListView):
    template_name = "transaction/amazon_order_list.html"
    model = models.AmazonOrder
    paginate_by = 20

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["additional_get_query"] = {}

        return context

    def get_queryset(self) -> QuerySet[Any]:
        query_set = (
            super()
            .get_queryset()
            .order_by("-date", "id")
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

        if self.request.GET.get("review_required"):
            query_set = query_set.filter(transaction=None)

        return query_set


amazon_order_list_view = AmazonOrderListView.as_view()


class AmazonOrderCreateView(LoginRequiredMixin, CreateView):
    template_name = "transaction/amazon_create.html"
    model = models.AmazonOrder
    form_class = money_forms.AmazonOrderForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        prev_order = models.AmazonOrder.objects.last()

        if prev_order:
            context["form"].initial["date"] = prev_order.date

        context["prev_order"] = prev_order

        return context

    def get_success_url(self) -> str:
        return reverse_lazy("money:amazon_order_create")


amazon_order_create_view = AmazonOrderCreateView.as_view()


class AmazonOrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "transaction/amazon_order_detail.html"
    model = models.AmazonOrder


amazon_order_detail_view = AmazonOrderDetailView.as_view()
