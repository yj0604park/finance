from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Max, Min, Prefetch, Sum
from django.db.models.functions.math import Sign
from django.shortcuts import render
from django.views.generic import DetailView, View

from money.choices import CurrencyType, TransactionCategory
from money.helpers.charts import get_transaction_chart_data
from money.helpers.helper import update_retailer_summary
from money.helpers.monthly import filter_month, update_month_info, update_month_summary
from money.models.accounts import Account
from money.models.stocks import StockTransaction
from money.models.transactions import Transaction, TransactionDetail


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

        context["data"] = get_transaction_chart_data(
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
        transaction_list = filter_month(request, transaction_list)

        date_range = Transaction.objects.aggregate(Min("date"), Max("date"))
        update_month_info(
            request,
            context,
            date_range["date__min"],
            date_range["date__max"],
        )

        update_month_summary(request, context, transaction_list)

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

        update_retailer_summary(context, context["retailer_detail"])

        context["category_list"] = TransactionCategory.choices
        context["currencies"] = [k[0] for k in CurrencyType.choices]

        return render(request, self.template_name, context)


category_detail_view = CategoryDetailView.as_view()
