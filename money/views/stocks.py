from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from money.forms import StockForm
from money.models.stocks import Stock, StockTransaction


class StockDetailView(LoginRequiredMixin, DetailView):
    model = Stock
    template_name = "stock/stock_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        stock = context["stock"]

        transaction_list = (
            StockTransaction.objects.filter(stock=stock)
            .prefetch_related("account")
            .order_by("date", "amount")
        )

        context["transaction_list"] = transaction_list
        return context


stock_detail_view = StockDetailView.as_view()


class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "stock/stock_create.html"


stock_create_view = StockCreateView.as_view()
