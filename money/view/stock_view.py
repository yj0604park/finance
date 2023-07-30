from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from money import helper, models


class StockAmountChartView(LoginRequiredMixin, ListView):
    template_name = "stock/stock_chart.html"
    model = models.StockTransaction

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # group by currency
        snapshot, stock_set = helper.get_stock_snapshot()
        context["labels"], context["datasets"] = helper.convert_snapshot_to_chart_data(
            snapshot, stock_set
        )
        return context


stock_amount_chart_view = StockAmountChartView.as_view()
