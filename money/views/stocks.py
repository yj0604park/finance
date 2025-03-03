from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from money.forms import StockForm
from money.helpers.charts import convert_snapshot_to_chart_data
from money.helpers.snapshots import get_stock_snapshot
from money.models.stocks import Stock, StockTransaction


class StockDetailView(LoginRequiredMixin, DetailView):
    model = Stock
    template_name = "stock/stock_detail.html"


stock_detail_view = StockDetailView.as_view()


class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "stock/stock_create.html"


stock_create_view = StockCreateView.as_view()


class StockAmountChartView(LoginRequiredMixin, ListView):
    template_name = "stock/stock_chart.html"
    model = StockTransaction

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # group by currency
        snapshot, stock_set = get_stock_snapshot()
        context["labels"], context["datasets"] = convert_snapshot_to_chart_data(
            snapshot, stock_set
        )
        return context


stock_amount_chart_view = StockAmountChartView.as_view()
