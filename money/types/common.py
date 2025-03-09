from dataclasses import dataclass
from decimal import Decimal

import strawberry


@strawberry.type
@dataclass
class BankBalance:
    """통화별 잔액을 나타내는 타입"""

    currency: str
    value: Decimal = strawberry.field(description="통화별 잔액")
