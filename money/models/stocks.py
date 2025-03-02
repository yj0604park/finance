from django.db import models
from django.urls import reverse
from django_choices_field import TextChoicesField

from money.choices import CurrencyType
from money.models.accounts import Account
from money.models.transactions import Transaction


class Stock(models.Model):
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=10, null=True, blank=True)
    currency = TextChoicesField(
        max_length=3, choices_enum=CurrencyType, default=CurrencyType.USD
    )

    class Meta:
        ordering = ["ticker"]

    def get_absolute_url(self):
        return reverse("money:stock_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.ticker}: {self.name}"


class StockTransaction(models.Model):
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    related_transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, null=True, blank=True
    )

    price = models.FloatField()
    shares = models.FloatField()
    amount = models.FloatField()
    balance = models.FloatField(default=0, null=True, blank=True)

    note = models.TextField(null=True, blank=True, default="")

    def get_absolute_url(self):
        return reverse("money:stock_transaction_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')}, Stock {self.stock}, share {self.shares}, price {self.price}"


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.FloatField()
