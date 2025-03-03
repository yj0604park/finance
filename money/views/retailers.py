from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, FloatField, Sum, When
from django.db.models.functions import TruncMonth
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView

from money.choices import CurrencyType, TransactionCategory
from money.forms import RetailerForm
from money.models.transactions import Retailer, Transaction


class RetailerSummaryView(LoginRequiredMixin, TemplateView):
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
