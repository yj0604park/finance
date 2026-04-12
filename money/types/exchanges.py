import strawberry
import strawberry.django
from strawberry import auto, relay

from money.models.exchanges import Exchange
from money.types.transactions import TransactionNode


@strawberry.django.filters.filter(Exchange, lookups=True)
class ExchangeFilter:
    date: auto
    exchange_type: auto


@strawberry.django.ordering.order(Exchange)
class ExchangeOrder:
    date: auto


@strawberry.django.type(Exchange, filters=ExchangeFilter, order=ExchangeOrder)
class ExchangeNode(relay.Node):
    id: relay.GlobalID
    date: auto
    from_transaction: TransactionNode
    to_transaction: TransactionNode
    from_amount: auto
    to_amount: auto
    from_currency: auto
    to_currency: auto
    ratio_per_krw: auto
    exchange_type: auto
