from django.db import models
from django_choices_field import TextChoicesField

from money.choices import CurrencyType, ExchangeType
from money.models.base import BaseTimeStampModel
from money.models.transactions import Transaction


class Exchange(BaseTimeStampModel):
    from_transaction = models.ForeignKey(
        Transaction, related_name="exchange_from", on_delete=models.CASCADE
    )
    to_transaction = models.ForeignKey(
        Transaction, related_name="exchange_to", on_delete=models.CASCADE
    )
    from_amount = models.DecimalField(max_digits=15, decimal_places=2)
    to_amount = models.DecimalField(max_digits=15, decimal_places=2)
    from_currency = TextChoicesField(max_length=3, choices_enum=CurrencyType)
    to_currency = TextChoicesField(max_length=3, choices_enum=CurrencyType)
    ratio_per_krw = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True
    )
    exchange_type = TextChoicesField(
        max_length=10, choices_enum=ExchangeType, default=ExchangeType.ETC
    )

    def __str__(self) -> str:
        return f"{self.date}: {self.ratio_per_krw}"
