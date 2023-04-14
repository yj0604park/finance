from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from money import models
from django import forms
from typing import Dict, Any, Optional, Type

import datetime

# Create your views here.
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


class BankDetailView(LoginRequiredMixin, DetailView):
    model = models.Bank
    template_name = "bank/bank_detail.html"


bank_detail_view = BankDetailView.as_view()


class BankListView(LoginRequiredMixin, ListView):
    model = models.Bank
    template_name = "bank/bank_list.html"


bank_list_view = BankListView.as_view()


def get_transaction_chart_data(transaction_list, recalculate=False):
    chart_dict = []
    sum = 0
    for transaction in transaction_list:
        sum += transaction.amount
        chart_dict.append(
            {
                "x": transaction.datetime.strftime("%Y-%m-%d"),
                "y": transaction.balance if not recalculate else sum,
            }
        )
    return chart_dict


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = models.Account
    template_name = "account/account_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["data"] = get_transaction_chart_data(
            context["account"].transaction_set.all().order_by("datetime", "-amount")
        )

        return context


account_detail_view = AccountDetailView.as_view()


class TransactionListView(LoginRequiredMixin, ListView):
    model = models.Transaction
    template_name = "transaction/transaction_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["data"] = get_transaction_chart_data(
            models.Transaction.objects.all().order_by("datetime", "-amount"),
            recalculate=True,
        )

        return context


transaction_list_view = TransactionListView.as_view()


def updateBalance(request, account_id):
    account = models.Account.objects.get(pk=account_id)
    transactions = account.transaction_set.all().order_by("datetime", "-amount")

    sum = 0
    for transaction in transactions:
        sum += transaction.amount
        transaction.balance = sum
        transaction.save()
        account.last_transaction = transaction.datetime

    account.amount = sum
    account.last_update = datetime.datetime.now()
    account.save()

    html = "<html><body>Updated</body></html>"
    return HttpResponse(html)


class TransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        exclude = ["balance"]


class TransactionFormView(CreateView):
    template_name = "transaction/transaction_add.html"
    model = models.Transaction
    form_class = TransactionForm

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


add_transaction_view = TransactionFormView.as_view()


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = models.Transaction
    template_name = "transaction/transaction_detail.html"


transaction_detail_view = TransactionDetailView.as_view()


class TransactionCategoryView(View):
    template_name = "dashboard/category.html"

    def get(self, request, *args, **kwargs):
        context = {
            "summarization": models.Transaction.objects.values("type").annotate(
                total_amount=-Sum("amount")
            ),
        }

        label = []
        data = []

        for summary in context["summarization"]:
            if summary["total_amount"] > 0:
                label.append(summary["type"])
                data.append(summary["total_amount"])
        context["label"] = label
        context["data"] = data

        return render(request, self.template_name, context)


transaction_category_view = TransactionCategoryView.as_view()
