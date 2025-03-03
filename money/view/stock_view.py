from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from money.helpers.charts import convert_snapshot_to_chart_data
from money.helpers.snapshots import get_stock_snapshot
from money.models.stocks import StockTransaction


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
