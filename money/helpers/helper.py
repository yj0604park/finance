import datetime
from decimal import Decimal

from django.db.models import Max, Q, Sum

from money.choices import AccountType, CurrencyType, RetailerType
from money.models.shoppings import Retailer
from money.models.transactions import Transaction


def filter_by_get(request, query_set, get_key_name, query_key_name):
    filter_value = request.GET.get(get_key_name)
    if filter_value:
        query_set = query_set.filter(**{query_key_name: filter_value})
    return query_set


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


def update_retailer_summary(context, retailer_list):
    label: dict[str, list[str]] = {k[0]: [] for k in CurrencyType.choices}
    data: dict[str, list[float]] = {k[0]: [] for k in CurrencyType.choices}

    for retailer in retailer_list:
        label[retailer["account__currency"]].append(str(retailer["retailer__name"]))
        data[retailer["account__currency"]].append(retailer["amount__sum"])

    context["label"] = label
    context["data"] = data
