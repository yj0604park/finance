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


@strawberry.type
class Mutation:
    create_account: types.AccountNode = mutations.create(types.AccountInput)
    create_transaction: types.TransactionNode = mutations.create(types.TransactionInput)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
