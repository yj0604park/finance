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
class AccountNode(relay.Node):
    id: relay.GlobalID
    name: auto
    bank: "BankNode"
    amount: auto
    type: auto
    currency: auto
    last_update: auto
    is_active: auto
    last_transaction: auto
    first_transaction: auto


@strawberry.django.input(models.Account)
class AccountInput:
    name: auto
    bank: "BankNode"
    type: auto
    currency: auto


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
class BankNode(relay.Node):
    id: relay.GlobalID
    name: auto
    balance: JSON
    account_set: strawberry.django.relay.ListConnectionWithTotalCount[
        AccountNode
    ] = strawberry.django.connection()


# endregion


@strawberry.django.type(models.Retailer)
class RetailerNode(relay.Node):
    id: relay.GlobalID
    name: auto
    category: auto


@strawberry.django.input(models.Retailer)
class RetailerInput:
    name: auto
    type: auto
    category: auto


# region: Transaction
@strawberry.django.filters.filter(models.Transaction, lookups=True)
class TransactionFilter:
    id: auto
    date: auto
    account: AccountFilter


@strawberry.django.ordering.order(models.Transaction)
class TransactionOrder:
    id: auto
    date: auto
    account: AccountOrder
    amount: auto


@strawberry.django.type(
    models.Transaction, filters=TransactionFilter, order=TransactionOrder
)
class TransactionNode(relay.Node):
    id: relay.GlobalID
    amount: auto
    account: AccountNode
    retailer: RetailerNode | None
    date: auto
    type: auto
    is_internal: auto
    requires_detail: auto
    reviewed: auto
    balance: auto
    type: auto
    note: auto
    related_transaction: "TransactionNode | None"


@strawberry.django.input(models.Transaction)
class TransactionInput:
    amount: auto
    account: AccountNode
    retailer: RetailerNode | None
    date: auto
    type: auto
    is_internal: auto
    note: auto


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
# region: Salary
@strawberry.django.filters.filter(models.Salary, lookups=True)
class SalaryFilter:
    id: auto
    date: auto


@strawberry.django.ordering.order(models.Salary)
class SalaryOrder:
    date: auto


@strawberry.django.type(models.Salary, filters=SalaryFilter, order=SalaryOrder)
class SalaryNode(relay.Node):
    id: relay.GlobalID
    date: auto
    gross_pay: auto
    total_adjustment: auto
    total_withheld: auto
    total_deduction: auto
    net_pay: auto

    pay_detail: JSON
    adjustment_detail: JSON
    tax_detail: JSON
    deduction_detail: JSON

    transaction: TransactionNode


# endregion


# region: Stock
@strawberry.django.input(models.Stock)
class StockInput:
    ticker: auto
    name: auto
    currency: auto


@strawberry.django.type(models.Stock)
class StockNode(relay.Node):
    id: relay.GlobalID
    ticker: auto
    name: auto
    currency: auto


# endregion
