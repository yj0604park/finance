# Standard library imports
from collections import defaultdict
from typing import Any, TypedDict

# Third-party library imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import (
    Case,
    Count,
    FloatField,
    Max,
    Min,
    OuterRef,
    Prefetch,
    QuerySet,
    Subquery,
    Sum,
    When,
)
from django.db.models.functions import TruncMonth
from django.db.models.functions.math import Sign
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView
from django_stubs_ext import WithAnnotations

from money import helper

# Local application/library specific imports
from money.choices import AccountType, CurrencyType, TransactionCategory
from money.forms import RetailerForm, SalaryForm, StockForm
from money.models.accounts import Account, AmountSnapshot, Bank
from money.models.exchanges import Exchange
from money.models.incomes import Salary
from money.models.stocks import Stock, StockPrice, StockTransaction
from money.models.transactions import Retailer, Transaction, TransactionDetail


# Dashboard
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        account_list = (
            Account.objects.filter(is_active=True)
            .prefetch_related("bank")
            .order_by("currency", "bank", "last_transaction", "amount")
            .annotate(
                null_count=Count(Case(When(transaction__balance__isnull=True, then=1))),
                unreviewed_count=Count(Case(When(transaction__reviewed=False, then=1))),
            )
        )
        account_list = helper.filter_by_get(
            self.request, account_list, "account_type", "type"
        )

        context["account_list"] = account_list
        context["sum_list"] = helper.get_transaction_summary(account_list)
        context["option_list"] = AccountType.choices

        return context


home_view = HomeView.as_view()


class BarAnnotations(TypedDict):
    last_stock_transaction: StockTransaction


# Bank related views
class BankDetailView(LoginRequiredMixin, DetailView):
    model = Bank
    template_name = "bank/bank_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        bank = context["bank"]
        account_list = Account.objects.filter(bank=bank, is_active=True).order_by(
            "type", "name"
        )

        # Get last stock transaction for each account
        last_stock_transaction = (
            StockTransaction.objects.filter(
                stock=OuterRef("stock"), account__name=OuterRef("account__name")
            )
            .order_by("-date", "amount")
            .values("balance")
        )

        # Get last stock price for each stock
        last_stock_price = (
            StockPrice.objects.filter(stock=OuterRef("stock"))
            .order_by("-date")
            .values("price")
        )

        # Annotate last stock transaction for each account
        last_transactions_per_account: QuerySet[WithAnnotations[Any]] = (
            StockTransaction.objects.filter(account__bank=bank)
            .distinct("stock", "account__name")
            .annotate(
                last_stock_transaction=Subquery(
                    last_stock_transaction[:1],
                    output_field=FloatField(),
                ),
                last_stock_price=Subquery(
                    last_stock_price[:1],
                    output_field=FloatField(),
                ),
            )
        )

        stock_balance_map = defaultdict(list)
        stock_value_map = defaultdict(float)
        for data in last_transactions_per_account:
            if (
                data.last_stock_transaction > 0.01
                or data.last_stock_transaction < -0.01
            ):
                stock_balance_map[data.account.pk].append(
                    (
                        data.stock.name,
                        data.last_stock_transaction,
                        data.last_stock_price,
                    )
                )
                if data.last_stock_price is not None:
                    stock_value_map[data.account.pk] += (
                        data.last_stock_transaction * data.last_stock_price
                    )

        context["account_list"] = account_list
        context["stock_balance_map"] = stock_balance_map
        context["stock_value_map"] = stock_value_map
        return context


bank_detail_view = BankDetailView.as_view()


class BankListView(LoginRequiredMixin, ListView):
    model = Bank
    template_name = "bank/bank_list.html"

    def get_queryset(self) -> QuerySet[Bank]:
        return super().get_queryset().annotate(count=Count("account")).order_by("name")


bank_list_view = BankListView.as_view()


# Account related views
class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = "account/account_detail.html"
    objects_per_page = 25

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .prefetch_related(
                Prefetch(
                    "transaction_set",
                    queryset=Transaction.objects.select_related("retailer"),
                )
            )
        )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = context["account"]
        ordered_transaction_set = (
            account.transaction_set.all()
            .prefetch_related(
                "retailer",
                "account",
            )
            .annotate(sign=Sign("amount") * Sum("balance"))
            .order_by("-date", "amount", "-sign")
        )

        context["additional_get_query"] = {}
        filter_reviewed = self.request.GET.get("reviewed")
        if filter_reviewed:
            ordered_transaction_set = ordered_transaction_set.filter(
                reviewed=filter_reviewed
            )
            context["additional_get_query"]["reviewed"] = filter_reviewed

        paginator = Paginator(ordered_transaction_set, self.objects_per_page)
        page_number = self.request.GET.get("page")
        page = paginator.get_page(page_number)
        context["page_obj"] = page

        context["data"] = helper.get_transaction_chart_data(
            ordered_transaction_set,
            account.currency,
            reverse=True,
        )

        context["stock_list"] = (
            StockTransaction.objects.filter(account=account)
            .order_by("-date", "balance")
            .prefetch_related("stock")
        )

        return context


account_detail_view = AccountDetailView.as_view()


class CategoryDetailView(LoginRequiredMixin, View):
    template_name = "category/category_detail.html"

    def get(self, request, *args, **kwargs):
        context: dict[str, Any] = {"additional_get_query": {}}
        category_type = kwargs["category_type"]
        context["print_all"] = request.GET.get("print_all", False)

        transaction_list = (
            Transaction.objects.filter(type=category_type)
            .filter(is_internal=False)
            .prefetch_related("retailer", "account")
            .order_by("date", "amount")
        )
        transaction_list = helper.filter_month(request, transaction_list)

        date_range = Transaction.objects.aggregate(Min("date"), Max("date"))
        helper.update_month_info(
            request,
            context,
            date_range["date__min"],
            date_range["date__max"],
        )

        helper.update_month_summary(request, context, transaction_list)

        context["category"] = category_type
        context["transaction_list"] = transaction_list
        context["unreviewd"] = transaction_list.filter(reviewed=False)

        context["retailer_detail"] = (
            transaction_list.values(
                "retailer__id", "retailer__name", "account__currency"
            )
            .annotate(Sum("amount"))
            .order_by("amount__sum")
        )
        context["detail_item_summary"] = (
            TransactionDetail.objects.filter(
                transaction__in=transaction_list.values("id")
            )
            .values("item__category")
            .annotate(Sum("amount"))
            .order_by("-amount__sum")
        )

        helper.update_retailer_summary(context, context["retailer_detail"])

        context["category_list"] = TransactionCategory.choices
        context["currencies"] = [k[0] for k in CurrencyType.choices]

        return render(request, self.template_name, context)


category_detail_view = CategoryDetailView.as_view()


class CompareCategoryView(LoginRequiredMixin, TemplateView):
    template_name = "category/compare_category.html"


compare_category_view = CompareCategoryView.as_view()


# Retailer related views
class RetailerSummaryView(LoginRequiredMixin, ListView):
    template_name = "retailer/retailer_summary.html"
    model = Retailer

    def get_queryset(self):
        currency = self.request.GET.get("currency", CurrencyType.USD)

        return (
            Transaction.objects.filter(account__currency=currency, is_internal=False)
            .values(
                "retailer__id", "retailer__name", "retailer__type", "retailer__category"
            )
            .annotate(
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
            .order_by("retailer__name")
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["currency"] = self.request.GET.get("currency", CurrencyType.USD)
        context["category_list"] = TransactionCategory.choices
        label = []
        data = []

        for transaction in context["transaction_list"]:
            if transaction["minus_sum"] < 0:
                label.append(transaction["retailer__name"])
                data.append(-transaction["minus_sum"])

        context["label"] = label
        context["data"] = data
        return context


retailer_summary_view = RetailerSummaryView.as_view()


class RetailerDetailView(LoginRequiredMixin, DetailView):
    template_name = "retailer/retailer_detail.html"
    model = Retailer

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        trnasactions = Transaction.objects.filter(
            retailer_id=self.kwargs["pk"]
        ).order_by("date")
        transactions_by_month = (
            trnasactions.annotate(month=TruncMonth("date"))
            .values("month", "account__currency")
            .annotate(total_amount=Sum("amount"))
            .order_by("month", "account__currency")
        )
        context["transactions"] = trnasactions
        context["transactions_by_month"] = transactions_by_month
        return context


retailer_detail_view = RetailerDetailView.as_view()


class RetailerCreateView(LoginRequiredMixin, CreateView):
    template_name = "retailer/retailer_create.html"
    model = Retailer
    form_class = RetailerForm

    def get_success_url(self) -> str:
        return reverse_lazy("money:retailer_create")


retailer_create_view = RetailerCreateView.as_view()


class SalaryListView(LoginRequiredMixin, ListView):
    template_name = "salary/salary_list.html"
    model = Salary

    def get_queryset(self):
        return super().get_queryset().order_by("date")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        net_pay = []
        gross_pay = []
        labels = []
        context["salary_list"] = context["salary_list"].order_by("-date")
        for salary in context["salary_list"]:
            labels.append(salary.date.strftime("%Y-%m-%d"))
            gross_pay.append(salary.gross_pay)
            net_pay.append(salary.net_pay)

        context["labels"] = labels
        context["datasets"] = {
            "labels": labels,
            "datasets": [
                {"label": "gross_pay", "data": gross_pay, "borderWidth": 1},
                {"label": "net_pay", "data": net_pay, "borderWidth": 1},
            ],
        }
        return context


salary_list_view = SalaryListView.as_view()


class SalaryDetailView(LoginRequiredMixin, DetailView):
    template_name = "salary/salary_detail.html"
    model = Salary

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        salary = context["salary"]
        valid_check = (
            ("Gross", salary.gross_pay, salary.pay_detail),
            ("Adjustment", salary.total_adjustment, salary.adjustment_detail),
            ("Tax", salary.total_withheld, salary.tax_detail),
            ("Deduction", salary.total_deduction, salary.deduction_detail),
        )

        valid = {}
        for key, total, detail in valid_check:
            diff = total - sum(detail.values())
            valid[key] = (diff, abs(diff) < 0.01)

        summary_diff = salary.net_pay - (
            salary.gross_pay
            + salary.total_adjustment
            + salary.total_withheld
            + salary.total_deduction
        )
        valid["Summary"] = (summary_diff, abs(summary_diff) < 0.01)
        valid["Transaction"] = (
            salary.transaction.amount - salary.net_pay,
            abs(salary.transaction.amount - salary.net_pay) < 0.01,
        )
        context["validity"] = valid
        return context


salary_detail_view = SalaryDetailView.as_view()


class SalaryCreateView(LoginRequiredMixin, CreateView):
    template_name = "salary/salary_create.html"
    model = Salary
    form_class = SalaryForm


salary_create_view = SalaryCreateView.as_view()


class StockCreateView(LoginRequiredMixin, CreateView):
    template_name = "stock/stock_create.html"
    model = Stock
    form_class = StockForm


stock_create_view = StockCreateView.as_view()


class StockDetailView(LoginRequiredMixin, DetailView):
    template_name = "stock/stock_detail.html"
    model = Stock


stock_detail_view = StockDetailView.as_view()


class ExchangeListView(LoginRequiredMixin, ListView):
    template_name = "exchange/exchange_list.html"
    model = Exchange
    paginate_by = 20

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["additional_get_query"] = {}

        return context

    def get_queryset(self) -> QuerySet[Exchange]:
        return super().get_queryset().order_by("-date")


exchange_list_view = ExchangeListView.as_view()


class AmountSnapshotListView(LoginRequiredMixin, ListView):
    """
    List snapshot of each day.
    """

    template_name = "snapshot/amount_snapshot.html"
    model = AmountSnapshot

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        stock_snapshot, _ = helper.get_stock_snapshot()
        stock_chart = [
            {"x": data["date"], "y": data["total"]} for data in stock_snapshot
        ]
        context["stock_data"] = stock_chart

        krw_chart = helper.snapshot_chart(
            context["amountsnapshot_list"], CurrencyType.KRW
        )
        usd_chart = helper.snapshot_chart(
            context["amountsnapshot_list"], CurrencyType.USD
        )

        # group by currency
        context["chart"] = {
            "KRW": krw_chart,
            "USD": usd_chart,
        }

        context["merged_chart"] = helper.merge_charts(usd_chart, stock_chart)

        return context


amount_snapshot_list_view = AmountSnapshotListView.as_view()
