import strawberry
import strawberry.django
from strawberry import auto, relay

from money.models.transactions import Retailer


@strawberry.django.filters.filter(Retailer, lookups=True)
class RetailerFilter:
    id: auto
    name: auto
    category: auto


@strawberry.django.type(Retailer, filters=RetailerFilter)
class RetailerNode(relay.Node):
    id: relay.GlobalID
    name: auto
    category: auto


@strawberry.django.input(Retailer)
class RetailerInput:
    name: auto
    type: auto
    category: auto
