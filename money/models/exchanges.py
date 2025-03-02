from django.db import models
from django.urls import reverse
from django_choices_field import TextChoicesField

from money.choices import CurrencyType, ExchangeType
from money.models.transactions import Transaction


class Exchange(models.Model):
    date = models.DateField()

    from_transaction = models.ForeignKey(
        Transaction, related_name="exchange_from", on_delete=models.CASCADE
    )
    to_transaction = models.ForeignKey(
        Transaction, related_name="exchange_to", on_delete=models.CASCADE
    )
    from_amount = models.FloatField()
    to_amount = models.FloatField()
    from_currency = TextChoicesField(max_length=3, choices_enum=CurrencyType)
    to_currency = TextChoicesField(max_length=3, choices_enum=CurrencyType)
    ratio_per_krw = models.FloatField(null=True, blank=True)
    exchange_type = TextChoicesField(
        max_length=10, choices_enum=ExchangeType, default=ExchangeType.ETC
    )

    def __str__(self) -> str:
        return f"{self.date}: {self.ratio_per_krw}"
