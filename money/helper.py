import datetime
from collections import defaultdict
from copy import copy

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
    total = 0

    sampling = transaction_list.count() > sample_threshold
    count = 0

    prev_month = (None, None)

    for transaction in transaction_list:
        count += 1
        total += transaction.amount

        if update_snapshot:
            new_month = (transaction.date.year, transaction.date.month)
            if new_month != prev_month:
                prev_month = new_month

        if not sampling or count % sample_ratio == 0:
            chart_dict.append(
                {
                    "x": transaction.date.strftime("%Y-%m-%d"),
                    "y": transaction.balance if not recalculate else total,
                }
            )

    if reverse:
        chart_dict.reverse()
    return chart_dict


def create_daily_snapshot():
    currency_list = models.CurrencyType.choices
    all_transaction_list = (
        models.Transaction.objects.all().order_by("date").prefetch_related("account")
    )

    for currency in currency_list:
        transaction_list = all_transaction_list.filter(account__currency=currency[0])
        if not transaction_list:
            continue

        prev_date = transaction_list[0].date
        total_value = 0.0

        history = defaultdict(float)
        for transaction in transaction_list:
            # Save previous date value
            if prev_date != transaction.date:
                create_snapshot(prev_date, currency[0], total_value, history)
                prev_date = transaction.date

            account_id = transaction.account.name
            account_value = history[account_id]
            account_value += transaction.amount

            # Update value in the map
            if account_value == 0.0:
                del history[account_id]
            else:
                history[account_id] = account_value
            total_value += transaction.amount

        # Last value will not be added by the above loop
        create_snapshot(prev_date, currency[0], total_value, history)


def create_snapshot(date, currency, amount, summary):
    if models.AmountSnapshot.objects.filter(date=date, currency=currency):
        snapshot = models.AmountSnapshot.objects.get(date=date, currency=currency)
        snapshot.amount = amount
        snapshot.summary = summary
    else:
        snapshot = models.AmountSnapshot(
            date=date, currency=currency, amount=amount, summary=summary
        )
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


def get_stock_snapshot():
    transaction_list = (
        models.StockTransaction.objects.all().order_by("date").prefetch_related("stock")
    )
    if not transaction_list:
        return []

    stock_transaction_data = []
    stock_name_set = set()

    total_amount = defaultdict(float)
    prev_date = transaction_list[0].date
    for transaction in transaction_list:
        stock_name_set.add(transaction.stock.name)

        # append prev date data
        if prev_date != transaction.date:
            stock_transaction_data.append((prev_date, copy(total_amount)))
            prev_date = transaction.date

        amount = total_amount[transaction.stock.name]
        amount += transaction.shares
        amount = round(amount, 5)
        if amount == 0.0:
            del total_amount[transaction.stock.name]
        else:
            total_amount[transaction.stock.name] = amount

    stock_transaction_data.append((prev_date, copy(total_amount)))

    return stock_transaction_data, stock_name_set


def convert_snapshot_to_chart_data(snapshot, stock_set: set):
    converted_data = defaultdict(list)  # Stock: Amount
    stock_list = list(stock_set)

    labels = []
    for date, stock_map in snapshot:  # Date: (Stock: Amount)
        labels.append(date.strftime("%Y-%m-%d"))
        for stock in stock_list:
            if stock in stock_map:
                converted_data[stock].append(stock_map[stock])
            else:
                converted_data[stock].append("NaN")

    datasets = []
    for stock in stock_list:
        data_string = ", ".join([str(x) for x in converted_data[stock]])
        datasets.append(
            f"{{label: '{stock}', data: [{data_string}], fill: false, tension: 0.1}}"
        )

    return labels, ", ".join(datasets)


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
