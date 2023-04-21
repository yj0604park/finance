from typing import Any, Dict, Optional, Type

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Sum, Case, When, FloatField
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from money import forms as money_forms
from money import helper, models


# Dashboard
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["account_list"] = (
            models.Account.objects.all().prefetch_related("bank").order_by("name")
        )

        sum = 0
        for account in context["account_list"]:
            sum += account.amount
        context["sum"] = sum
        return context


home_view = HomeView.as_view()


# Bank related views
class BankDetailView(LoginRequiredMixin, DetailView):
    model = models.Bank
    template_name = "bank/bank_detail.html"


bank_detail_view = BankDetailView.as_view()


class BankListView(LoginRequiredMixin, ListView):
    model = models.Bank
    template_name = "bank/bank_list.html"


bank_list_view = BankListView.as_view()


# Account related views
class AccountDetailView(LoginRequiredMixin, DetailView):
    model = models.Account
    template_name = "account/account_detail.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                Prefetch(
                    "transaction_set",
                    queryset=models.Transaction.objects.select_related("retailer"),
                )
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ordered_transaction_set"] = (
            context["account"]
            .transaction_set.all()
            .prefetch_related("retailer", "account")
            .order_by("-datetime", "amount")
        )

        context["data"] = helper.get_transaction_chart_data(
            context["ordered_transaction_set"],
            reverse=True,
        )

        return context


account_detail_view = AccountDetailView.as_view()


# Transaction related views
class TransactionListView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "transaction/transaction_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["data"] = helper.get_transaction_chart_data(
            models.Transaction.objects.all().order_by("datetime", "-amount"),
            recalculate=True,
        )

        return context


transaction_list_view = TransactionListView.as_view()


class TransactionCreateView(LoginRequiredMixin, CreateView):
    template_name = "transaction/transaction_add.html"
    model = models.Transaction
    form_class = money_forms.TransactionForm

    def get_success_url(self) -> str:
        return reverse_lazy(
            "money:add_transaction", kwargs={"account_id": self.kwargs["account_id"]}
        )

    def get_form(self) -> forms.BaseModelForm:
        form = super().get_form()
        form.initial["account"] = self.kwargs["account_id"]
        datetime_default = self.request.GET.get("datetime", None)
        if datetime_default:
            form.initial["datetime"] = datetime_default

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_transaction = models.Transaction.objects.filter(
            account_id=self.kwargs["account_id"]
        ).order_by("-datetime", "amount")[0]
        if latest_transaction:
            context["form"].initial["datetime"] = latest_transaction.datetime.strftime(
                "%Y-%m-%d"
            )
        context["latest_transaction"] = latest_transaction
        return context


add_transaction_view = TransactionCreateView.as_view()


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = models.Transaction
    template_name = "transaction/transaction_detail.html"


transaction_detail_view = TransactionDetailView.as_view()


# Transaction category related views
class TransactionCategoryView(LoginRequiredMixin, View):
    template_name = "dashboard/category.html"

    def get(self, request, *args, **kwargs):
        context = {
            "summarization": models.Transaction.objects.values("type")
            .annotate(total_amount=-Sum("amount"))
            .order_by("-total_amount"),
        }

        label = []
        data = []

        income = []

        for summary in context["summarization"]:
            if summary["total_amount"] > 0:
                label.append(summary["type"])
                data.append(summary["total_amount"])
            else:
                income.append(summary)
        context["label"] = label
        context["data"] = data
        context["income"] = income

        return render(request, self.template_name, context)


transaction_category_view = TransactionCategoryView.as_view()


class CategoryDetailView(LoginRequiredMixin, View):
    template_name = "dashboard/category_detail.html"

    def get(self, request, *args, **kwargs):
        print(kwargs)
        category_type = kwargs["category_type"]
        transaction_list = (
            models.Transaction.objects.filter(type=category_type)
            .prefetch_related("retailer", "account")
            .order_by("datetime", "amount")
        )
        context = {"type": category_type, "transactions": transaction_list}
        return render(request, self.template_name, context)


category_detail_view = CategoryDetailView.as_view()


# Transaction review related views
class ReviewTransactionView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "review/review_transaction.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs.filter(reviewed=False)
            .order_by("datetime", "amount")
            .prefetch_related("account")
        )
        return qs


review_transaction_view = ReviewTransactionView.as_view()


# Retailer related views
class RetailerSummaryView(LoginRequiredMixin, ListView):
    template_name = "retailer/retailer_summary.html"
    model = models.Retailer

    def get_queryset(self):
        return (
            models.Transaction.objects.values(
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
            .order_by("minus_sum")
        )


retailer_summary_view = RetailerSummaryView.as_view()


class RetailerDetailView(LoginRequiredMixin, DetailView):
    template_name = "retailer/retailer_detail.html"
    model = models.Retailer


retailer_detail_view = RetailerDetailView.as_view()
