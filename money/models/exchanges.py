from django.db import models

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
    ratio_per_krw = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True
    )

    from_currency = models.CharField(
        max_length=3,
        choices=CurrencyType.choices,
    )
    to_currency = models.CharField(
        max_length=3,
        choices=CurrencyType.choices,
    )

    exchange_type = models.CharField(
        max_length=20,
        choices=ExchangeType.choices,
        default=ExchangeType.ETC,
    )

    def __str__(self):
        return f"{self.date}: {self.from_currency} {self.from_amount} -> {self.to_currency} {self.to_amount}"
