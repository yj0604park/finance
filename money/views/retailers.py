from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Min
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView

from money.forms import RetailerForm
from money.helpers.helper import filter_by_get
from money.helpers.monthly import filter_month, update_month_info, update_month_summary
from money.models.transactions import Retailer, Transaction


class RetailerSummaryView(LoginRequiredMixin, TemplateView):
    template_name = "retailer/retailer_summary.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        retailer_list = Retailer.objects.all().order_by("name")
        retailer_list = filter_by_get(
            self.request, retailer_list, "retailer_type", "type"
        )

        context["retailer_list"] = retailer_list
        return context


retailer_summary_view = RetailerSummaryView.as_view()


class RetailerDetailView(LoginRequiredMixin, DetailView):
    model = Retailer
    template_name = "retailer/retailer_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        retailer = context["retailer"]

        transaction_list = (
            Transaction.objects.filter(retailer=retailer)
            .prefetch_related("account")
            .order_by("date", "amount")
        )
        transaction_list = filter_month(self.request, transaction_list)

        date_range = Transaction.objects.aggregate(Min("date"), Max("date"))
        update_month_info(
            self.request,
            context,
            date_range["date__min"],
            date_range["date__max"],
        )

        update_month_summary(self.request, context, transaction_list)

        context["transaction_list"] = transaction_list
        return context


retailer_detail_view = RetailerDetailView.as_view()


class RetailerCreateView(LoginRequiredMixin, CreateView):
    model = Retailer
    form_class = RetailerForm
    template_name = "retailer/retailer_create.html"
    success_url = reverse_lazy("money:retailer_summary")


retailer_create_view = RetailerCreateView.as_view()
