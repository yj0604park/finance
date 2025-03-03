from typing import Any, cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from money.models.exchanges import Exchange


class ExchangeListView(LoginRequiredMixin, ListView):
    model = Exchange
    template_name = "exchange/exchange_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        exchange_list = cast(QuerySet[Exchange], context["exchange_list"])
        context["exchange_list"] = exchange_list.order_by("-date")
        return context


exchange_list_view = ExchangeListView.as_view()
