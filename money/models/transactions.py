from django.db import models
from django.urls import reverse
from django_choices_field import TextChoicesField

from money.choices import DetailItemCategory, RetailerType, TransactionCategory
from money.models.accounts import Account
from money.models.base import BaseAmountModel, BaseTimeStampModel, BaseURLModel
from money.models.shoppings import DetailItem, Retailer


class Transaction(BaseTimeStampModel, BaseAmountModel, BaseURLModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    retailer = models.ForeignKey(
        Retailer, on_delete=models.SET_NULL, blank=True, null=True
    )
    balance = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    note = models.TextField(null=True, blank=True)
    is_internal = models.BooleanField(default=False)
    requires_detail = models.BooleanField(default=False)

    type = TextChoicesField(
        max_length=30,
        choices_enum=TransactionCategory,
        default=TransactionCategory.ETC,
    )
    reviewed = models.BooleanField(default=False)

    related_transaction = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )

    def get_absolute_url(self):
        return reverse("money:transaction_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'{self.pk} {self.date.strftime("%Y-%m-%d")} '
            + f"{self.account.name}: "
            + f"{self.retailer.name if self.retailer else None}"
        )


class TransactionDetail(BaseAmountModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item = models.ForeignKey(DetailItem, on_delete=models.CASCADE)
    note = models.CharField(max_length=40, blank=True, null=True)
    count = models.DecimalField(max_digits=10, decimal_places=2, default=1)


class TransactionFile(BaseTimeStampModel):
    file = models.FileField(upload_to="transaction_files/")
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True
    )
    note = models.TextField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    processed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.date}: {self.file.name}"
