import datetime
from collections import defaultdict
from copy import copy
from decimal import Decimal
from math import floor
from typing import DefaultDict

from dateutil.rrule import MONTHLY, rrule
from django.db.models import Max, Q, Sum
from django.db.models.functions import TruncMonth
from django.db.models.query import QuerySet

from money.choices import AccountType, CurrencyType, RetailerType
from money.models.accounts import AmountSnapshot
from money.models.incomes import Salary
from money.models.stocks import StockTransaction
from money.models.transactions import Retailer, Transaction


def get_transaction_chart_data(
    transaction_list: QuerySet[Transaction],
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
    total = Decimal(0.0)

    sampling = transaction_list.count() > sample_threshold
    count = 0

    prev_month: tuple[int | None, int | None] = (None, None)

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
                    "y": str(transaction.balance) if not recalculate else total,
                }
            )

    if reverse:
        chart_dict.reverse()
    return chart_dict


def create_daily_snapshot() -> None:
    currency_list = CurrencyType.choices
    all_transaction_list = (
        Transaction.objects.all().order_by("date").prefetch_related("account")
    )

    for currency in currency_list:
        transaction_list = all_transaction_list.filter(account__currency=currency[0])
        if not transaction_list:
            continue

        prev_date = transaction_list[0].date
        total_value = Decimal(0.0)

        history: DefaultDict[str, Decimal] = defaultdict(Decimal)
        for transaction in transaction_list:
            # Save previous date value
            if prev_date != transaction.date:
                create_snapshot(prev_date, currency[0], total_value, history)
                prev_date = transaction.date

            account_id = transaction.account.name
            account_value = history[account_id]
            account_value = floor(
                (account_value + transaction.amount) * Decimal(100)
            ) / Decimal(100)

            # Update value in the map
            if account_value == 0.0:
                del history[account_id]
            else:
                history[account_id] = account_value
            total_value += transaction.amount

        # Last value will not be added by the above loop
        create_snapshot(prev_date, currency[0], total_value, history)


def create_snapshot(date, currency, amount: Decimal, summary):
    float_summary = {k: str(v) for k, v in summary.items()}
    amount = floor(amount * Decimal(100)) / Decimal(100)
    if AmountSnapshot.objects.filter(date=date, currency=currency):
        snapshot = AmountSnapshot.objects.get(date=date, currency=currency)
        snapshot.amount = amount
        snapshot.summary = float_summary
    else:
        snapshot = AmountSnapshot(
            date=date, currency=currency, amount=amount, summary=float_summary
        )
    snapshot.save()


def snapshot_chart(snapshot_list: QuerySet[AmountSnapshot], currency):
    chart_info = []
    snapshot_list = snapshot_list.filter(currency=currency).order_by("date")
    for snapshot in snapshot_list:
        chart_info.append(
            {
                "x": snapshot.date.strftime("%Y-%m-%d"),
                "y": str(snapshot.amount),
            }
        )
    return chart_info


def get_stock_snapshot():
    transaction_list = (
        StockTransaction.objects.filter(account__currency=CurrencyType.USD)
        .order_by("date", "shares")
        .prefetch_related("stock")
    )
    if not transaction_list:
        return []

    stock_transaction_data = []
    stock_name_set = set()

    total_balance: DefaultDict[str, Decimal] = defaultdict(Decimal)
    price_info: DefaultDict[str, Decimal] = defaultdict(Decimal)
    prev_date = transaction_list[0].date
    for transaction in transaction_list:
        stock_name_set.add(transaction.stock.name)

        # append prev date data
        if prev_date != transaction.date:
            today_total = Decimal(0.0)
            for stock_name, stock_amount in total_balance.items():
                today_total += stock_amount * price_info[stock_name]

            stock_transaction_data.append(
                {
                    "date": prev_date.strftime("%Y-%m-%d"),
                    "balance": copy(total_balance),
                    "price": copy(price_info),
                    "total": round(today_total, 2),
                }
            )
            prev_date = transaction.date

        amount = total_balance[transaction.stock.name]
        amount += transaction.shares
        amount = round(amount, 5)
        if amount == 0.0:
            del total_balance[transaction.stock.name]
            del price_info[transaction.stock.name]
        else:
            total_balance[transaction.stock.name] = amount
            price_info[transaction.stock.name] = transaction.price

    today_total = Decimal(0.0)
    for stock_name, stock_amount in total_balance.items():
        today_total += stock_amount * price_info[stock_name]
    stock_transaction_data.append(
        {
            "date": prev_date.strftime("%Y-%m-%d"),
            "balance": copy(total_balance),
            "price": copy(price_info),
            "total": round(today_total, 2),
        }
    )

    return stock_transaction_data, list(stock_name_set)


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

        month_label: dict[str, list[str]] = {k[0]: [] for k in CurrencyType.choices}
        month_data: dict[str, list[str]] = {k[0]: [] for k in CurrencyType.choices}

        for month in month_detail:
            month_label[month["account__currency"]].append(
                f"{month['month'].year}년 {month['month'].month}월"
            )
            month_data[month["account__currency"]].append(month["total_amount"])

        context["month_detail"] = month_detail
        context["month_label"] = month_label
        context["month_data"] = month_data


def update_retailer_summary(context, retailer_list):
    label: dict[str, list[str]] = {k[0]: [] for k in CurrencyType.choices}
    data: dict[str, list[float]] = {k[0]: [] for k in CurrencyType.choices}

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
    sum_dict: dict[str, dict[str, Decimal]] = {
        k[0]: {"current": Decimal(0.0), "prev": Decimal(0.0)}
        for k in CurrencyType.choices
    }

    currency_map = {}
    for account in account_list:
        currency_map[account.id] = account.currency
        sum_dict[account.currency]["current"] += account.amount

    # compare with last month
    last_prev_month_day = datetime.date.today().replace(day=1) - datetime.timedelta(
        days=1
    )

    prev_transaction_list_per_account = (
        Transaction.objects.filter(
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
        first_transaction = (
            Transaction.objects.filter(account__id=account["account"])
            .filter(date=account["last_date"])
            .order_by("balance")
            .first()
        )

        if first_transaction is not None:
            balance = first_transaction.balance

            if balance:
                sum_dict[currency_map[account["account"]]]["prev"] += balance

    sum_list = [(k, v) for k, v in sum_dict.items()]
    for _, v in sum_list:
        v["diff"] = v["current"] - v["prev"]
        v["ratio"] = round(
            v["diff"] / (v["prev"] if v["prev"] else Decimal(1.0)) * Decimal(100.0), 2
        )
    sum_list.sort()

    return sum_list


def filter_by_get(request, query_set, get_key_name, query_key_name):
    filter_value = request.GET.get(get_key_name)
    if filter_value:
        query_set = query_set.filter(**{query_key_name: filter_value})
    return query_set


def filter_by_currency(data_list, currency):
    """
    Filter data_list by currency and return total value
    """
    filtered_list = list(filter(lambda x: x[0].currency == currency, data_list))

    return {
        "filtered_list": sorted(
            filtered_list,
            key=lambda x: (
                x[0].first_transaction
                if x[0].first_transaction
                else datetime.date.today()
            ),
        ),
        "total_last_value_positive": sum(
            [x[1]["last_value"] for x in filtered_list if x[1]["last_value"] > 0]
        ),
        "total_max_value_positive": sum(
            [x[1]["max_value"] for x in filtered_list if x[1]["max_value"] > 0]
        ),
        "count": len(filtered_list),
    }


def get_saving_interest_tax_summary(target_year: int):
    tax_interest = (
        Transaction.objects.prefetch_related("account")
        .filter(
            date__year=target_year,
            account__type=AccountType.INSTALLMENT_SAVING,
            retailer__isnull=False,
        )
        .order_by("date", "-amount")
    )

    account = {}

    for transaction in tax_interest:
        if transaction.account not in account:
            account[transaction.account] = {
                "total_interest": Decimal(0.0),
                "total_tax": Decimal(0.0),
                "after_tax": Decimal(0.0),
            }

        account[transaction.account]["after_tax"] += transaction.amount

        if transaction.amount > 0:
            account[transaction.account]["total_interest"] += transaction.amount

        else:
            account[transaction.account]["total_tax"] += transaction.amount

    return sorted(account.items(), key=lambda x: x[0].name)


def bank_summary(target_year: int):
    """
    Get all transactions in the year and return summary.
    """

    banks = Retailer.objects.filter(type=RetailerType.BANK)
    bank_interest = (
        Transaction.objects.filter(
            retailer__type=RetailerType.BANK, date__year=target_year
        )
        .values("retailer__name")
        .annotate(total=Sum("amount"))
        .order_by("retailer")
    )

    return {"banks": banks, "bank_interest": bank_interest}


def year_summary(target_year: int):
    """
    Get all transactions in the year and return summary.
    """
    this_year_transactions = (
        Transaction.objects.prefetch_related("account")
        .filter(date__year=target_year, account__bank__id=5)
        .order_by("date", "-amount")
    )

    account_summary = {}

    for transaction in this_year_transactions:
        account = transaction.account
        if account not in account_summary:
            account_summary[account] = {
                "max_value": 0.0,
                "max_date": None,
                "last_value": 0.0,
            }

        if transaction.balance is not None:
            current_max = account_summary[account]["max_value"]

            if current_max < transaction.balance:
                account_summary[account]["max_value"] = max(
                    current_max, transaction.balance
                )
                account_summary[account]["max_date"] = transaction.date

            account_summary[account]["last_value"] = transaction.balance
        else:
            print(f"{transaction} is not updated")

    account_summary = account_summary.items()

    # Salary summary
    salary = Salary.objects.filter(date__year=target_year)
    salary_info = {
        "total_grosspay": Decimal(0.0),
        "401(K)": 0.0,
        "federal_tax": 0.0,
        "patent_award": 0.0,
        "vacation_payout": 0.0,
        "social_security_tax": 0.0,
        "medicare_tax": 0.0,
        "stock_award": 0.0,
        "relocation": 0.0,
        "total_pay_detail": defaultdict(float),
        "total_adjustment_detail": defaultdict(float),
        "total_tax_detail": defaultdict(float),
        "total_deduction_detail": defaultdict(float),
    }

    for s in salary:
        salary_info["total_grosspay"] += s.gross_pay
        if "Patent Award" in s.pay_detail:
            salary_info["patent_award"] += s.pay_detail["Patent Award"]
        if "Vacation Payout" in s.pay_detail:
            salary_info["vacation_payout"] += s.pay_detail["Vacation Payout"]

        salary_info["401(K)"] += s.adjustment_detail["401(K)"]
        if "Stock Award Income" in s.adjustment_detail:
            salary_info["stock_award"] += s.adjustment_detail["Stock Award Income"]
        if "Relo expense - taxable" in s.adjustment_detail:
            salary_info["relocation"] += s.adjustment_detail["Relo expense - taxable"]
        if "Relo Expense Total Taxes" in s.adjustment_detail:
            salary_info["relocation"] += s.adjustment_detail["Relo Expense Total Taxes"]

        salary_info["federal_tax"] -= s.tax_detail["Federal income tax"]
        if "Social security tax" in s.tax_detail:
            salary_info["social_security_tax"] -= s.tax_detail["Social security tax"]
        if "Medicare tax" in s.tax_detail:
            salary_info["medicare_tax"] -= s.tax_detail["Medicare tax"]

        for k, v in s.pay_detail.items():
            salary_info["total_pay_detail"][k] += v
        for k, v in s.adjustment_detail.items():
            salary_info["total_adjustment_detail"][k] += v
        for k, v in s.tax_detail.items():
            salary_info["total_tax_detail"][k] += v
        for k, v in s.deduction_detail.items():
            salary_info["total_deduction_detail"][k] += v

    context = {
        "target_year": target_year,
        "this_year_transactions": this_year_transactions,
        "account_summary_krw": filter_by_currency(account_summary, CurrencyType.KRW),
        "account_summary_usd": filter_by_currency(account_summary, CurrencyType.USD),
        "saving_interest_tax": get_saving_interest_tax_summary(target_year),
        "salary": salary_info,
        "bank": bank_summary(target_year),
    }

    return context


def merge_charts(chart_a, chart_b):
    merged_chart = []
    current_value = defaultdict(float)
    pos_a = 0
    pos_b = 0
    while True:
        if pos_a >= len(chart_a) and pos_b >= len(chart_b):
            break

        if pos_a < len(chart_a) and pos_b < len(chart_b):
            if chart_a[pos_a]["x"] < chart_b[pos_b]["x"]:
                current_value["a"] = chart_a[pos_a]["y"]

                merged_chart.append(
                    {
                        "x": chart_a[pos_a]["x"],
                        "y": float(current_value["a"]) + float(current_value["b"]),
                    }
                )
                pos_a += 1
            else:
                current_value["b"] = chart_b[pos_b]["y"]

                merged_chart.append(
                    {
                        "x": chart_b[pos_b]["x"],
                        "y": float(current_value["a"]) + float(current_value["b"]),
                    }
                )
                pos_b += 1

        elif pos_a < len(chart_a):
            merged_chart.append(
                {
                    "x": chart_a[pos_a]["x"],
                    "y": float(current_value["a"]) + float(current_value["b"]),
                }
            )
            pos_a += 1

        else:
            merged_chart.append(
                {
                    "x": chart_b[pos_b]["x"],
                    "y": float(current_value["a"]) + float(current_value["b"]),
                }
            )
            pos_b += 1

    return merged_chart
