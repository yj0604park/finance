from collections import defaultdict

from django.db import models
from django.urls import reverse

from money.choices import AccountType
from money.models.base import BaseAmountModel, BaseCurrencyModel


class Account(BaseAmountModel, BaseCurrencyModel):
    """
    Model for a bank account.
    """

    bank = models.ForeignKey("Bank", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_collation="C")
    alias = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.CHECKING_ACCOUNT,
    )

    last_update = models.DateTimeField(null=True, blank=True)
    last_transaction = models.DateField(null=True, blank=True)
    first_transaction = models.DateField(null=True, blank=True)
    first_added = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bank.name} {self.name}"

    def get_absolute_url(self):
        return reverse("money:account_detail", kwargs={"pk": self.pk})

    def account_type(self):
        return self.type


class Bank(models.Model):
    """
    Model for a bank.
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @property
    def balance(self):
        sum_dict = defaultdict(float)

        for account in Account.objects.filter(bank=self):
            sum_dict[account.currency] += account.amount
        return sum_dict


class AmountSnapshot(BaseAmountModel, BaseCurrencyModel):
    date = models.DateField()
    summary = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.date}: {self.currency}"
