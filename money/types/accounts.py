import strawberry
import strawberry.django
from strawberry import auto, relay

from money.models.accounts import Account, AmountSnapshot, Bank
from money.types.common import BankBalance


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
    balance: list[BankBalance]

    account_set: strawberry.django.relay.ListConnectionWithTotalCount[AccountNode] = (
        strawberry.django.connection()
    )


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
