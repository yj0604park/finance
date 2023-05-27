import datetime
import calendar
from collections import defaultdict

from dateutil.rrule import MONTHLY, rrule
from django.db.models import Max, Q, Sum
from django.db.models.functions import TruncMonth
from django.db.models.query import QuerySet

from money import models


def get_transaction_chart_data(
    transaction_list: QuerySet[models.Transaction],
    currency,
    recalculate=False,
    reverse=False,
    sample_threshold=1000,
    sample_ratio=50,
    update_snapshot=False,
):
    """Create chart of transaction amounts. transaction_list should be sorted by date."""
    transaction_list = transaction_list.filter(account__currency=currency)

    chart_dict = []
    sum = 0

    sampling = transaction_list.count() > sample_threshold
    count = 0

    prev_month = None

    for transaction in transaction_list:
        count += 1
        sum += transaction.amount

        if update_snapshot:
            new_month = (transaction.date.year, transaction.date.month)
            if new_month != prev_month:
                if prev_month:
                    _, last_day = calendar.monthrange(prev_month[0], prev_month[1])
                    create_snapshot(
                        f"{prev_month[0]:04d}-{prev_month[1]:02d}-{last_day:02d}",
                        currency,
                        sum,
                    )
                prev_month = new_month

        if not sampling or count % sample_ratio == 0:
            chart_dict.append(
                {
                    "x": transaction.date.strftime("%Y-%m-%d"),
                    "y": transaction.balance if not recalculate else sum,
                }
            )

    if prev_month:
        _, last_day = calendar.monthrange(prev_month[0], prev_month[1])
        create_snapshot(
            f"{prev_month[0]:04d}-{prev_month[1]:02d}-{last_day:02d}", currency, sum
        )

    if reverse:
        chart_dict.reverse()
    return chart_dict


def create_snapshot(date, currency, amount):
    if models.AmountSnapshot.objects.filter(date=date, currency=currency):
        snapshot = models.AmountSnapshot.objects.get(date=date, currency=currency)
        snapshot.amount = amount
    else:
        snapshot = models.AmountSnapshot(date=date, currency=currency, amount=amount)
    snapshot.save()


def snapshot_chart(snapshot_list: QuerySet[models.AmountSnapshot], currency):
    chart_info = []
    snapshot_list = snapshot_list.filter(currency=currency).order_by("date")
    for snapshot in snapshot_list:
        chart_info.append(
            {
                "x": snapshot.date.strftime("%Y-%m-%d"),
                "y": snapshot.amount,
            }
        )
    return chart_info


def filter_month(request, query_set):
    # month should given as YYYY-mm
    selected_month = request.GET.get("month")

    if selected_month:
        selected_month_split = selected_month.split("-")

        query_set = query_set.filter(
            date__year=selected_month_split[0], date__month=selected_month_split[1]
        )
    return query_set


def update_month_info(request, context, start_date, end_date):
    # update context, selected month info and return query set

    selected_month = request.GET.get("month")

    if selected_month:
        selected_month_split = selected_month.split("-")

        context["selected_month"] = (
            selected_month,
            f"{selected_month_split[0]}년 {selected_month_split[1]}월",
        )

        context["additional_get_query"]["month"] = selected_month

    context["months"] = get_month_list(start_date, end_date)


def update_month_summary(request, context, query_set):
    # get monthly summary of transactions if month is not specified
    selected_month = request.GET.get("month")
    if not selected_month:
        month_detail = (
            query_set.annotate(month=TruncMonth("date"))
            .values("month", "account__currency")
            .annotate(total_amount=Sum("amount"))
            .order_by("month")
        )

        month_label = {k[0]: [] for k in models.CurrencyType.choices}
        month_data = {k[0]: [] for k in models.CurrencyType.choices}

        for month in month_detail:
            month_label[month["account__currency"]].append(
                f"{month['month'].year}년 {month['month'].month}월"
            )
            month_data[month["account__currency"]].append(month["total_amount"])

        context["month_detail"] = month_detail
        context["month_label"] = month_label
        context["month_data"] = month_data


def update_retailer_summary(context, retailer_list):
    label = {k[0]: [] for k in models.CurrencyType.choices}
    data = {k[0]: [] for k in models.CurrencyType.choices}

    for retailer in retailer_list:
        label[retailer["account__currency"]].append(str(retailer["retailer__name"]))
        data[retailer["account__currency"]].append(retailer["amount__sum"])

    context["label"] = label
    context["data"] = data


def get_month_list(start_date, end_date):
    months = [
        (dt.year, dt.strftime("%Y-%m"))
        for dt in rrule(MONTHLY, dtstart=start_date, until=end_date)
    ]
    month_per_year = defaultdict(list)

    for year, month in months:
        month_per_year[year].append(month)
    return month_per_year


def get_transaction_summary(account_list):
    sum_dict = {k[0]: {"current": 0, "prev": 0} for k in models.CurrencyType.choices}

    currency_map = {}
    for account in account_list:
        currency_map[account.id] = account.currency
        sum_dict[account.currency]["current"] += account.amount

    # compare with last month
    last_prev_month_day = datetime.date.today().replace(day=1) - datetime.timedelta(
        days=1
    )

    prev_transaction_list_per_account = (
        models.Transaction.objects.filter(
            Q(
                date__month__lte=last_prev_month_day.month,
                date__year=last_prev_month_day.year,
            )
            | Q(date__year__lt=last_prev_month_day.year)
        )
        .filter(account__id__in=currency_map.keys())
        .values("account")
        .annotate(
            last_date=Max("date"),
        )
    )

    for account in prev_transaction_list_per_account:
        balance = (
            models.Transaction.objects.filter(account__id=account["account"])
            .filter(date=account["last_date"])
            .order_by("balance")
            .first()
            .balance
        )

        if balance:
            sum_dict[currency_map[account["account"]]]["prev"] += balance

    sum_list = [(k, v) for k, v in sum_dict.items()]
    for _, v in sum_list:
        v["diff"] = v["current"] - v["prev"]
        v["ratio"] = round(v["diff"] / (v["prev"] if v["prev"] else 1) * 100, 2)
    sum_list.sort()

    return sum_list


def filter_by_get(request, query_set, get_key_name, query_key_name):
    filter_value = request.GET.get(get_key_name)
    if filter_value:
        query_set = query_set.filter(**{query_key_name: filter_value})
    return query_set
