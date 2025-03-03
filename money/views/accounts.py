from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Max, Min, Prefetch, Sum
from django.db.models.functions.math import Sign
from django.shortcuts import render
from django.views.generic import DetailView, View

from money import helper
from money.models.accounts import Account
from money.models.stocks import StockTransaction
from money.models.transactions import Transaction


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
        return render(request, self.template_name, context)


category_detail_view = CategoryDetailView.as_view()
