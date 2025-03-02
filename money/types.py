import strawberry
import strawberry.django
from strawberry import auto, relay
from strawberry.scalars import JSON

from money.models import shoppings, stocks
from money.models.accounts import Account, AmountSnapshot, Bank
from money.models.incomes import Salary
from money.models.transactions import Retailer, Transaction


# region Account
@strawberry.django.filters.filter(Account, lookups=True)
class AccountFilter:
    id: auto
    name: auto
    bank: "BankFilter"
    amount: auto
    type: auto
    currency: auto
    last_update: auto
    is_active: auto


@strawberry.django.ordering.order(Account)
class AccountOrder:
    name: auto
    bank: "BankOrder"
    last_update: auto


@strawberry.django.type(
    Account, filters=AccountFilter, pagination=True, order=AccountOrder
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


@strawberry.django.input(Account)
class AccountInput:
    name: auto
    bank: "BankNode"
    type: auto
    currency: auto


# endregion
# region: Bank
@strawberry.django.filters.filter(Bank, lookups=True)
class BankFilter:
    id: auto
    name: auto


@strawberry.django.ordering.order(Bank)
class BankOrder:
    name: auto


@strawberry.django.type(Bank, filters=BankFilter)
class BankNode(relay.Node):
    id: relay.GlobalID
    name: auto
    balance: JSON
    account_set: strawberry.django.relay.ListConnectionWithTotalCount[AccountNode] = (
        strawberry.django.connection()
    )


# endregion


@strawberry.django.type(Retailer)
class RetailerNode(relay.Node):
    id: relay.GlobalID
    name: auto
    category: auto


@strawberry.django.input(Retailer)
class RetailerInput:
    name: auto
    type: auto
    category: auto


# region: Transaction
@strawberry.django.filters.filter(Transaction, lookups=True)
class TransactionFilter:
    id: auto
    date: auto
    account: AccountFilter


@strawberry.django.ordering.order(Transaction)
class TransactionOrder:
    id: auto
    date: auto
    account: AccountOrder
    amount: auto
    balance: auto


@strawberry.django.type(Transaction, filters=TransactionFilter, order=TransactionOrder)
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

    @strawberry.field
    def get_sorting_amount(self) -> float:
        return self.balance if self.amount >= 0 else -self.balance


@strawberry.django.input(Transaction)
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
@strawberry.django.filters.filter(AmountSnapshot, lookups=True)
class AmountSnapshotFilter:
    id: auto
    date: auto
    currency: auto


@strawberry.django.ordering.order(AmountSnapshot)
class AmountSnapshotOrder:
    name: auto
    date: auto


@strawberry.django.type(
    AmountSnapshot, filters=AmountSnapshotFilter, order=AmountSnapshotOrder
)
class AmountSnapshotNode(relay.Node):
    id: relay.GlobalID
    date: auto
    currency: auto
    amount: auto
    summary: auto


# endregion
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


# endregion
# region: Salary
@strawberry.django.filters.filter(Salary, lookups=True)
class SalaryFilter:
    id: auto
    date: auto


@strawberry.django.ordering.order(Salary)
class SalaryOrder:
    date: auto


@strawberry.django.type(Salary, filters=SalaryFilter, order=SalaryOrder)
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

# region: Amazon Orders


@strawberry.django.input(shoppings.AmazonOrder)
class AmazonOrderInput:
    date: auto
    item: auto
    is_returned: auto
    transaction: TransactionNode
    return_transaction: TransactionNode | None


@strawberry.django.ordering.order(shoppings.AmazonOrder)
class AmazonOrderOrder:
    date: auto


@strawberry.django.type(shoppings.AmazonOrder, order=AmazonOrderOrder)
class AmazonOrderNode(relay.Node):
    id: relay.GlobalID
    date: auto
    item: auto
    is_returned: auto
    transaction: TransactionNode | None
    return_transaction: TransactionNode | None


# endregion


@strawberry.type()
class SalarySummaryNode:
    year: auto
    total_gross_pay: auto
