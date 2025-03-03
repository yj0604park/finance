from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from money.choices import CurrencyType
from money.helpers.charts import merge_charts, snapshot_chart
from money.helpers.snapshots import get_stock_snapshot
from money.models.accounts import AmountSnapshot


class AmountSnapshotListView(LoginRequiredMixin, ListView):
    """
    List snapshot of each day.
    """

    template_name = "snapshot/amount_snapshot.html"
    model = AmountSnapshot

    def get_context_data(self, **kwargs: Any) -> dict[str, list[Any]]:
        context = super().get_context_data(**kwargs)

        stock_snapshot, _ = get_stock_snapshot()
        stock_chart: list[dict[str, str]] = [
            {"x": str(data["date"]), "y": str(data["total"])} for data in stock_snapshot
        ]
        context["stock_data"] = stock_chart

        krw_chart = snapshot_chart(context["amountsnapshot_list"], CurrencyType.KRW)
        usd_chart = snapshot_chart(context["amountsnapshot_list"], CurrencyType.USD)

        # group by currency
        context["chart"] = {
            "KRW": krw_chart,
            "USD": usd_chart,
        }

        context["merged_chart"] = merge_charts(usd_chart, stock_chart)

        return context


amount_snapshot_list_view = AmountSnapshotListView.as_view()
