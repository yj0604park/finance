from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from money.models.exchanges import Exchange


class ExchangeListView(LoginRequiredMixin, ListView):
    template_name = "exchange/exchange_list.html"
    model = Exchange
    paginate_by = 20

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["additional_get_query"] = {}

        return context

    def get_queryset(self) -> QuerySet[Exchange]:
        return super().get_queryset().order_by("-date")


exchange_list_view = ExchangeListView.as_view()
