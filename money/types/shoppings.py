import strawberry
import strawberry.django
from strawberry import auto, relay

from money.models.shoppings import AmazonOrder
from money.types.transactions import TransactionNode


# region: Amazon Orders
@strawberry.django.input(AmazonOrder)
class AmazonOrderInput:
    date: auto
    item: auto
    is_returned: auto
    transaction: TransactionNode
    return_transaction: TransactionNode | None


@strawberry.django.ordering.order(AmazonOrder)
class AmazonOrderOrder:
    date: auto


@strawberry.django.type(AmazonOrder, order=AmazonOrderOrder)
class AmazonOrderNode(relay.Node):
    id: relay.GlobalID
    date: auto
    item: auto
    is_returned: auto
    transaction: TransactionNode | None
    return_transaction: TransactionNode | None


# endregion
