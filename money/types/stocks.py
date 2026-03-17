import strawberry
import strawberry.django
from strawberry import auto, relay

from money.models import stocks
from money.types.accounts import AccountFilter, AccountNode
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
@strawberry.django.filters.filter(stocks.StockTransaction, lookups=True)
class StockTransactionFilter:
    id: auto
    stock: StockFilter
    account: AccountFilter
    date: auto


@strawberry.django.ordering.order(stocks.StockTransaction)
class StockTransactionOrder:
    date: auto
    price: auto


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


@strawberry.django.type(
    stocks.StockTransaction, filters=StockTransactionFilter, order=StockTransactionOrder
)
class StockTransactionNode(relay.Node):
    id: relay.GlobalID
    date: auto
    account: AccountNode
    stock: StockNode
    related_transaction: TransactionNode

    price: auto
    amount: auto
    shares: auto
    balance: auto
    note: auto


@strawberry.django.input(stocks.StockTransaction, partial=True)
class StockTransactionPartialInput:
    id: relay.GlobalID
    related_transaction: TransactionNode | None


# endregion


# region: StockPrice
@strawberry.django.filters.filter(stocks.StockPrice, lookups=True)
class StockPriceFilter:
    id: auto
    stock: StockFilter
    date: auto


@strawberry.django.ordering.order(stocks.StockPrice)
class StockPriceOrder:
    date: auto
    price: auto


@strawberry.django.input(stocks.StockPrice)
class StockPriceInput:
    date: auto
    stock: StockNode
    price: auto


@strawberry.django.type(
    stocks.StockPrice, filters=StockPriceFilter, order=StockPriceOrder
)
class StockPriceNode(relay.Node):
    id: relay.GlobalID
    date: auto
    stock: StockNode
    price: auto


# endregion
