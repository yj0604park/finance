from django.db import models

from money.choices import DetailItemCategory, RetailerType, TransactionCategory
from money.models.base import BaseTimeStampModel, BaseURLModel


class Retailer(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(
        max_length=20,
        choices=RetailerType.choices,
        default=RetailerType.ETC,
    )
    category = models.CharField(
        max_length=30,
        choices=TransactionCategory.choices,
        default=TransactionCategory.ETC,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.type}: {self.name}"


class DetailItem(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(
        max_length=10,
        choices=DetailItemCategory.choices,
        default=DetailItemCategory.ETC,
    )

    def __str__(self):
        return f"{self.category}-{self.name}"

    class Meta:
        ordering = ["name"]


class AmazonOrder(BaseTimeStampModel, BaseURLModel):
    item = models.TextField()
    is_returned = models.BooleanField(default=False)
    transaction = models.ForeignKey(
        "money.Transaction",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    return_transaction = models.ForeignKey(
        "money.Transaction",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="returned_order",
    )

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} {self.item}"
