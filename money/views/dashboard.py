from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, Count, When
from django.views.generic import TemplateView

from money.choices import AccountType
from money.helpers.helper import filter_by_get, get_transaction_summary
from money.models.accounts import Account


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        account_list = (
            Account.objects.filter(is_active=True)
            .prefetch_related("bank")
            .order_by("currency", "bank", "last_transaction", "amount")
            .annotate(
                null_count=Count(Case(When(transaction__balance__isnull=True, then=1))),
                unreviewed_count=Count(Case(When(transaction__reviewed=False, then=1))),
            )
        )

        account_list = filter_by_get(self.request, account_list, "account_type", "type")

        context["account_list"] = account_list
        context["sum_list"] = get_transaction_summary(account_list)
        context["option_list"] = AccountType.choices

        return context


home_view = HomeView.as_view()
