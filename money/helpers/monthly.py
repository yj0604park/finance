from datetime import datetime
from typing import Any

from dateutil.rrule import MONTHLY, rrule
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models.query import QuerySet
from django.http import HttpRequest


def filter_month(request: HttpRequest, query_set: QuerySet) -> QuerySet:
    # month should given as YYYY-mm
    selected_month = request.GET.get("month")

    if selected_month:
        selected_month_split = selected_month.split("-")

        query_set = query_set.filter(
            date__year=selected_month_split[0], date__month=selected_month_split[1]
        )
    return query_set


def update_month_info(
    request: HttpRequest,
    context: dict[str, Any],
    start_date: datetime,
    end_date: datetime,
) -> None:
    # update context, selected month info and return query set
    selected_month = request.GET.get("month")

    if selected_month:
        selected_month_split = selected_month.split("-")

        context["selected_month"] = (
            selected_month,
            f"{selected_month_split[0]}년 {selected_month_split[1]}월",
        )

        context["additional_get_query"]["month"] = selected_month

    context["months"] = _get_month_list(start_date, end_date)


def update_month_summary(
    request: HttpRequest, context: dict[str, Any], query_set: QuerySet
) -> None:
    # get monthly summary of transactions if month is not specified
    selected_month = request.GET.get("month")
    if not selected_month:
        month_detail = (
            query_set.annotate(month=TruncMonth("date"))
            .values("month", "account__currency")
            .annotate(total_amount=Sum("amount"))
            .order_by("month")
        )

        context["month_detail"] = month_detail


def _get_month_list(start_date: datetime, end_date: datetime) -> list[tuple[str, str]]:
    month_list = []
    for dt in rrule(MONTHLY, dtstart=start_date, until=end_date):
        month_list.append(
            (
                dt.strftime("%Y-%m"),
                f"{dt.year}년 {dt.month}월",
            )
        )
    return month_list
