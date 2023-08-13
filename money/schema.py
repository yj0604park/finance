import strawberry
import strawberry.django
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry_django.relay import ListConnectionWithTotalCount

from money import types


@strawberry.type
class Query:
    transactions: list[types.Transaction] = strawberry.django.field()
    retailers: list[types.Retailer] = strawberry.django.field()

    bank_relay: ListConnectionWithTotalCount[
        types.BankNode
    ] = strawberry.django.connection()
    account_relay: ListConnectionWithTotalCount[
        types.AccountNode
    ] = strawberry.django.connection()
    amountSnapshot_relay: ListConnectionWithTotalCount[
        types.AmountSnapshotNode
    ] = strawberry.django.connection()


schema = strawberry.Schema(
    query=Query,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
