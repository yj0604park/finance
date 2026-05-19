import strawberry
import strawberry.django
from strawberry import auto, relay

from money.models.credit_cards import CreditCard, CreditCardBenefit
from money.types.accounts import AccountNode


@strawberry.django.filters.filter(CreditCard, lookups=True)
class CreditCardFilter:
    id: auto


@strawberry.django.ordering.order(CreditCard)
class CreditCardOrder:
    annual_fee: auto
    issue_date: auto


@strawberry.django.type(CreditCardBenefit)
class CreditCardBenefitNode(relay.Node):
    id: relay.GlobalID
    category: auto
    title: auto
    description: auto
    rate: auto
    cap_amount: auto
    conditions: auto


@strawberry.django.type(CreditCard, filters=CreditCardFilter, order=CreditCardOrder)
class CreditCardNode(relay.Node):
    id: relay.GlobalID
    account: AccountNode
    annual_fee: auto
    issue_date: auto
    expiry_date: auto
    notes: auto
    benefits: list[CreditCardBenefitNode]


@strawberry.django.input(CreditCard)
class CreditCardInput:
    account: auto
    annual_fee: auto
    issue_date: auto
    expiry_date: auto
    notes: str = ""


@strawberry.django.input(CreditCardBenefit)
class CreditCardBenefitInput:
    credit_card: auto
    category: auto
    title: auto
    description: str = ""
    rate: auto
    cap_amount: auto
    conditions: str = ""
