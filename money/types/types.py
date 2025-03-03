import strawberry
import strawberry.django
from strawberry import auto


@strawberry.type()
class SalarySummaryNode:
    year: auto
    total_gross_pay: auto
