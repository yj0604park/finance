from django.db import models
from django_choices_field import TextChoicesField

from money.choices import DetailItemCategory, RetailerType, TransactionCategory
from money.models.base import BaseTimeStampModel, BaseURLModel


class Retailer(models.Model):
    name = models.CharField(max_length=30)
    type = TextChoicesField(
        max_length=20, choices_enum=RetailerType, default=RetailerType.ETC
    )
    category = TextChoicesField(
        max_length=30,
        choices_enum=TransactionCategory,
        default=TransactionCategory.ETC,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.type}: {self.name}"


class DetailItem(models.Model):
    name = models.CharField(max_length=30)
    category = TextChoicesField(
        max_length=10,
        choices_enum=DetailItemCategory,
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
