from django.db import models
from django.urls import reverse
from django_choices_field import TextChoicesField

from money.choices import DetailItemCategory, RetailerType, TransactionCategory
from money.models.accounts import Account


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


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    retailer = models.ForeignKey(
        Retailer, on_delete=models.SET_NULL, blank=True, null=True
    )
    amount = models.FloatField()
    amount_int = models.BigIntegerField(default=0)

    balance = models.FloatField(null=True, blank=True)
    date = models.DateField()
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
        self.amount_int = int(self.amount * 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'{self.pk} {self.date.strftime("%Y-%m-%d")} '
            + f"{self.account.name}: "
            + f"{self.retailer.name if self.retailer else None}"
        )


class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item = models.ForeignKey(DetailItem, on_delete=models.CASCADE)

    note = models.CharField(max_length=40, blank=True, null=True)
    amount = models.FloatField()
    count = models.FloatField(default=1)


class TransactionFile(models.Model):
    file = models.FileField(upload_to="transaction_files/")
    date = models.DateField()
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True
    )
    note = models.TextField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    processed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.date}: {self.file.name}"
