from typing import Any, Dict, Optional, Type

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from money import forms as money_forms
from money import helper, models


# Dashboard
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["account_list"] = models.Account.objects.all().order_by("name")

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
        return super().get_queryset().prefetch_related("transaction_set")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["data"] = helper.get_transaction_chart_data(
            context["account"].transaction_set.all().order_by("datetime", "-amount")
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

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

    def get_form(self) -> forms.BaseModelForm:
        form = super().get_form()
        form.initial["account"] = self.kwargs["account_id"]
        datetime_default = self.request.GET.get("datetime", None)
        if datetime_default:
            form.initial["datetime"] = datetime_default
        return form


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


class CategoryDetailView(View):
    template_name = "dashboard/category_detail.html"

    def get(self, request, *args, **kwargs):
        print(kwargs)
        category_type = kwargs["category_type"]
        transaction_list = models.Transaction.objects.filter(
            type=category_type
        ).order_by("datetime", "amount")
        context = {"type": category_type, "transactions": transaction_list}
        return render(request, self.template_name, context)


category_detail_view = CategoryDetailView.as_view()

# Transaction review related views
class ReviewTransactionView(ListView):
    model = models.Transaction
    template_name = "review/review_transaction.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(reviewed=False).order_by("datetime", "amount")
        return qs


review_transaction_view = ReviewTransactionView.as_view()
