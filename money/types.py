import strawberry
import strawberry.django
from strawberry import auto, relay
from strawberry.scalars import JSON

from money import models


# region Account
@strawberry.django.filters.filter(models.Account, lookups=True)
class AccountFilter:
    id: auto
    name: auto
    bank: "BankFilter"
    amount: auto
    type: auto
    currency: auto
    last_update: auto
    is_active: auto


@strawberry.django.ordering.order(models.Account)
class AccountOrder:
    name: auto
    bank: "BankOrder"
    last_update: auto


@strawberry.django.type(
    models.Account, filters=AccountFilter, pagination=True, order=AccountOrder
)
class Account:
    id: auto
    name: auto
    bank: "Bank"
    amount: auto
    type: auto
    currency: auto
    last_update: auto
    is_active: auto


@strawberry.django.type(
    models.Account, filters=AccountFilter, pagination=True, order=AccountOrder
)
class AccountNode(relay.Node):
    id: relay.GlobalID
    name: auto
    bank: "BankNode"
    amount: auto
    type: auto
    currency: auto
    last_update: auto
    is_active: auto


# endregion
# region: Bank
@strawberry.django.filters.filter(models.Bank, lookups=True)
class BankFilter:
    id: auto
    name: auto


@strawberry.django.ordering.order(models.Bank)
class BankOrder:
    name: auto


@strawberry.django.type(models.Bank, filters=BankFilter)
class Bank:
    id: auto
    name: auto
    account_set: list[Account]
    balance: JSON


@strawberry.django.type(models.Bank, filters=BankFilter)
class BankNode(relay.Node):
    id: relay.GlobalID
    name: auto
    balance: JSON
    account_set: strawberry.django.relay.ListConnectionWithTotalCount[
        AccountNode
    ] = strawberry.django.connection()


# endregion


@strawberry.django.type(models.Retailer)
class Retailer:
    id: auto
    name: auto


# region: Transaction
@strawberry.django.filters.filter(models.Transaction, lookups=True)
class TransactionFilter:
    id: auto
    date: auto


@strawberry.django.type(models.Transaction, filters=TransactionFilter)
class Transaction:
    id: auto
    amount: auto
    retailer: Retailer | None
    is_internal: auto


# endregion


# region: Snapshot
@strawberry.django.filters.filter(models.AmountSnapshot, lookups=True)
class AmountSnapshotFilter:
    id: auto
    date: auto
    currency: auto


@strawberry.django.ordering.order(models.AmountSnapshot)
class AmountSnapshotOrder:
    name: auto
    date: auto


@strawberry.django.type(
    models.AmountSnapshot, filters=AmountSnapshotFilter, order=AmountSnapshotOrder
)
class AmountSnapshotNode(relay.Node):
    id: relay.GlobalID
    date: auto
    currency: auto
    amount: auto
    summary: auto


# endregion
# region: Stock
@strawberry.django.filters.filter(models.Stock, lookups=True)
class StockFilter:
    id: auto
    name: auto


@strawberry.django.type(models.Stock, filters=StockFilter)
class Stock:
    id: auto
    name: auto
    ticker: auto
    currency: auto


# endregion
