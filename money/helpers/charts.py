from decimal import Decimal
from typing import Any

from django.db.models.query import QuerySet

from money.models.accounts import AmountSnapshot
from money.models.transactions import Transaction


def get_transaction_chart_data(
    transaction_list: QuerySet[Transaction],
    currency: str,
    recalculate: bool = False,
    reverse: bool = False,
    sample_threshold: int = 1000,
    sample_ratio: int = 50,
    update_snapshot: bool = False,
) -> list[dict[str, str]]:
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
                    "y": str(transaction.balance) if not recalculate else str(total),
                }
            )

    if reverse:
        chart_dict.reverse()
    return chart_dict


def snapshot_chart(
    snapshot_list: QuerySet[AmountSnapshot], currency: str
) -> list[dict[str, str]]:
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


def convert_snapshot_to_chart_data(
    snapshot: list[Any], stock_set: set[str]
) -> tuple[list[str], str]:
    from collections import defaultdict

    converted_data: defaultdict[str, list[str]] = defaultdict(list)  # Stock: Amount
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
