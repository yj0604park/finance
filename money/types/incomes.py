import strawberry
import strawberry.django
from strawberry import auto, relay
from strawberry.scalars import JSON

from money.models.incomes import Salary
from money.types.transactions import TransactionNode


# region: Salary
@strawberry.django.filters.filter(Salary, lookups=True)
class SalaryFilter:
    id: auto
    date: auto


@strawberry.django.ordering.order(Salary)
class SalaryOrder:
    date: auto


@strawberry.django.type(Salary, filters=SalaryFilter, order=SalaryOrder)
class SalaryNode(relay.Node):
    id: relay.GlobalID
    date: auto
    gross_pay: auto
    total_adjustment: auto
    total_withheld: auto
    total_deduction: auto
    net_pay: auto

    pay_detail: JSON
    adjustment_detail: JSON
    tax_detail: JSON
    deduction_detail: JSON

    transaction: TransactionNode


# endregion
