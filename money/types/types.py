from decimal import Decimal

import strawberry


@strawberry.type()
class SalarySummaryNode:
    year: int
    total_gross_pay: Decimal
