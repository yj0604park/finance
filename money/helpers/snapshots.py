from collections import defaultdict
from copy import copy
from decimal import Decimal
from typing import DefaultDict

from money.choices import CurrencyType
from money.models.accounts import AmountSnapshot
from money.models.stocks import StockTransaction
from money.models.transactions import Transaction


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
            account_value = account_value + transaction.amount

            # Update value in the map
            if account_value == 0.0:
                del history[account_id]
            else:
                history[account_id] = account_value
            total_value += transaction.amount

        # Last value will not be added by the above loop
        create_snapshot(prev_date, currency[0], total_value, history)


def create_snapshot(
    date: str, currency: str, amount: Decimal, summary: DefaultDict[str, Decimal]
) -> None:
    float_summary = {k: str(v) for k, v in summary.items()}
    if AmountSnapshot.objects.filter(date=date, currency=currency):
        snapshot = AmountSnapshot.objects.get(date=date, currency=currency)
        snapshot.amount = amount
        snapshot.summary = float_summary
    else:
        snapshot = AmountSnapshot(
            date=date, currency=currency, amount=amount, summary=float_summary
        )
    snapshot.save()


def get_stock_snapshot() -> tuple[list[dict], list[str]]:
    transaction_list = (
        StockTransaction.objects.filter(account__currency=CurrencyType.USD)
        .order_by("date", "shares")
        .prefetch_related("stock")
    )
    if not transaction_list:
        return [], []

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
