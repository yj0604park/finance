import strawberry
import strawberry.django
from strawberry import auto, relay

from money.models.shoppings import AmazonOrder, Retailer
from money.types.transactions import TransactionNode


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
