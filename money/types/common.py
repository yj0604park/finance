from dataclasses import dataclass

import strawberry


@strawberry.type
@dataclass
class BankBalance:
    """통화별 잔액을 나타내는 타입"""

    currency: str
    value: float
