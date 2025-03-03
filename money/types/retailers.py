import strawberry
import strawberry.django
from strawberry import auto, relay

from money.models.transactions import Retailer


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
