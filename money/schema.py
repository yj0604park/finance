import strawberry
import strawberry.django
from strawberry_django import mutations
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry_django.relay import ListConnectionWithTotalCount

from money import types


@strawberry.type
class Query:
    transaction_relay: ListConnectionWithTotalCount[
        types.TransactionNode
    ] = strawberry.django.connection()

    retailer_relay: ListConnectionWithTotalCount[
        types.RetailerNode
    ] = strawberry.django.connection()

    bank_relay: ListConnectionWithTotalCount[
        types.BankNode
    ] = strawberry.django.connection()

    account_relay: ListConnectionWithTotalCount[
        types.AccountNode
    ] = strawberry.django.connection()

    amountSnapshot_relay: ListConnectionWithTotalCount[
        types.AmountSnapshotNode
    ] = strawberry.django.connection()

    salary_relay: ListConnectionWithTotalCount[
        types.SalaryNode
    ] = strawberry.django.connection()

    stock_relay: ListConnectionWithTotalCount[
        types.StockNode
    ] = strawberry.django.connection()

    amazon_order_relay: ListConnectionWithTotalCount[
        types.AmazonOrderNode
    ] = strawberry.django.connection()


@strawberry.type
class Mutation:
    create_account: types.AccountNode = mutations.create(types.AccountInput)
    create_transaction: types.TransactionNode = mutations.create(types.TransactionInput)
    create_retailer: types.RetailerNode = mutations.create(types.RetailerInput)
    create_stock: types.StockNode = mutations.create(types.StockInput)
    create_stock_transaction: types.StockTransactionNode = mutations.create(
        types.StockTransactionInput
    )


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
