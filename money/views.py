from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, FloatField, Prefetch, Sum, When
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView

from money import forms as money_forms
from money import helper, models


# Dashboard
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["account_list"] = (
            models.Account.objects.all()
            .prefetch_related("bank")
            .order_by("currency", "name")
        )

        sum_dict = {k[0]: 0 for k in models.CurrencyType.choices}

        for account in context["account_list"]:
            sum_dict[account.currency] += account.amount
        sum_list = [(k, v) for k, v in sum_dict.items()]
        sum_list.sort()

        context["sum_list"] = sum_list
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


class DetailItemCreateView(LoginRequiredMixin, CreateView):
    template_name = "detail_item/detail_item_create.html"
    model = models.DetailItem
    form_class = money_forms.DetailItemForm

    def get_success_url(self) -> str:
        return reverse_lazy("money:detail_item_create")


detail_item_create_view = DetailItemCreateView.as_view()


class CategoryDetailView(LoginRequiredMixin, View):
    template_name = "dashboard/category_detail.html"

    def get(self, request, *args, **kwargs):
        category_type = kwargs["category_type"]
        transaction_list = (
            models.Transaction.objects.filter(type=category_type)
            .prefetch_related("retailer", "account")
            .order_by("datetime", "amount")
        )
        context = {
            "type": category_type,
            "transactions": transaction_list,
        }
        return render(request, self.template_name, context)


category_detail_view = CategoryDetailView.as_view()


# Retailer related views
class RetailerSummaryView(LoginRequiredMixin, ListView):
    template_name = "retailer/retailer_summary.html"
    model = models.Retailer

    def get_queryset(self):
        currency = self.request.GET.get("currency", models.CurrencyType.USD)

        return (
            models.Transaction.objects.filter(
                account__currency=currency, is_internal=False
            )
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
            .order_by("minus_sum")
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["currency"] = self.request.GET.get("currency", models.CurrencyType.USD)
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
    model = models.Retailer

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["transactions"] = models.Transaction.objects.filter(
            retailer_id=self.kwargs["pk"]
        ).order_by("datetime")
        return context


retailer_detail_view = RetailerDetailView.as_view()


class RetailerCreateView(LoginRequiredMixin, CreateView):
    template_name = "retailer/retailer_create.html"
    model = models.Retailer
    form_class = money_forms.RetailerForm

    def get_success_url(self) -> str:
        return reverse_lazy("money:retailer_create")


retailer_create_view = RetailerCreateView.as_view()


class SalaryListView(LoginRequiredMixin, ListView):
    template_name = "salary/salary_list.html"
    model = models.Salary


salary_list_view = SalaryListView.as_view()


class SalaryDetailView(LoginRequiredMixin, DetailView):
    template_name = "salary/salary_detail.html"
    model = models.Salary

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
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
        context["validity"] = valid
        return context


salary_detail_view = SalaryDetailView.as_view()


class SalaryCreateView(LoginRequiredMixin, CreateView):
    template_name = "salary/salary_create.html"
    model = models.Salary
    form_class = money_forms.SalaryForm


salary_create_view = SalaryCreateView.as_view()
