import strawberry
import strawberry.django
from strawberry import auto, relay

from money.models import stocks
from money.types.accounts import AccountNode
from money.types.transactions import TransactionNode


# region: Stock
@strawberry.django.filters.filter(stocks.Stock, lookups=True)
class StockFilter:
    id: auto
    name: auto


@strawberry.django.type(stocks.Stock, filters=StockFilter)
class Stock:
    id: auto
    name: auto
    ticker: auto
    currency: auto


@strawberry.django.input(stocks.Stock)
class StockInput:
    ticker: auto
    name: auto
    currency: auto


@strawberry.django.type(stocks.Stock)
class StockNode(relay.Node):
    id: relay.GlobalID
    ticker: auto
    name: auto
    currency: auto


# endregion


# region: StockTransaction
@strawberry.django.input(stocks.StockTransaction)
class StockTransactionInput:
    date: auto
    account: AccountNode
    stock: StockNode
    related_transaction: TransactionNode

    price: auto
    amount: auto
    shares: auto
    note: auto


@strawberry.django.type(stocks.StockTransaction)
class StockTransactionNode(relay.Node):
    id: relay.GlobalID
    account: AccountNode
    stock: StockNode
    related_transaction: TransactionNode

    price: auto
    amount: auto
    shares: auto
    note: auto


# endregion
