from collections import defaultdict
from typing import Any, cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, FloatField, OuterRef, QuerySet, Subquery
from django.views.generic import DetailView, ListView
from django_stubs_ext import WithAnnotations

from money.models.accounts import Account, Bank
from money.models.stocks import StockPrice, StockTransaction


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
        qs = cast(QuerySet[Bank], super().get_queryset())
        return qs.annotate(count=Count("account")).order_by("name")


bank_list_view = BankListView.as_view()
