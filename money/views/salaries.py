from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from money.forms import SalaryForm
from money.models.incomes import Salary


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
