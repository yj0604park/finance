from typing import Any, cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from money.models.accounts import AmountSnapshot


class AmountSnapshotListView(LoginRequiredMixin, ListView):
    model = AmountSnapshot
    template_name = "snapshot/snapshot_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        snapshot_list = cast(QuerySet[AmountSnapshot], context["snapshot_list"])
        context["snapshot_list"] = snapshot_list.order_by("-date")
        return context


amount_snapshot_list_view = AmountSnapshotListView.as_view()
