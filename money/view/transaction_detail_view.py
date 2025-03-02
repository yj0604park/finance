from typing import Any

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Prefetch, QuerySet, Sum
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from money import forms as money_forms
from money.models import models
from money.models.transaction import DetailItem, Transaction, TransactionDetail


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
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
                    queryset=TransactionDetail.objects.all().select_related("item"),
                )
            )
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
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
    model = TransactionDetail
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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
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


class DetailItemListView(LoginRequiredMixin, ListView):
    template_name = "detail_item/detail_item_list.html"
    model = DetailItem

    def get_queryset(self) -> QuerySet[Any]:
        group_by_category = (
            DetailItem.objects.all()
            .values("category")
            .annotate(name_array=ArrayAgg("name", distinct=False))
            .order_by("category")
        )

        for v in group_by_category:
            list.sort(v["name_array"])

        return group_by_category


detail_item_list_view = DetailItemListView.as_view()


class DetailItemCreateView(LoginRequiredMixin, CreateView):
    template_name = "detail_item/detail_item_create.html"
    model = DetailItem
    form_class = money_forms.DetailItemForm

    def get_success_url(self) -> str:
        return reverse_lazy("money:detail_item_create")


detail_item_create_view = DetailItemCreateView.as_view()


class DetailItemCategoryView(LoginRequiredMixin, TemplateView):
    template_name = "detail_item/detail_item_category.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = self.kwargs["category"]
        context["category"] = category
        category_model = TransactionDetail.objects.filter(item__category=category)
        context["summary"] = category_model.aggregate(Sum("amount"))
        context["per_item"] = (
            category_model.values("item__name").annotate(Sum("amount")).order_by()
        )
        return context


detail_item_category_view = DetailItemCategoryView.as_view()
