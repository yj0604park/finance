from decimal import Decimal

from django.db import models

from money.models.accounts import Account
from money.models.base import (
    BaseAmountModel,
    BaseCurrencyModel,
    BaseTimeStampModel,
    BaseURLModel,
)
from money.models.transactions import Transaction


class Stock(BaseURLModel, BaseCurrencyModel):
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ["ticker"]

    def __str__(self):
        return f"{self.ticker}: {self.name}"


class StockTransaction(BaseTimeStampModel, BaseAmountModel, BaseURLModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    related_transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, null=True, blank=True
    )

    price = models.DecimalField(max_digits=15, decimal_places=2)
    shares = models.DecimalField(max_digits=15, decimal_places=4)
    balance = models.DecimalField(
        max_digits=15, decimal_places=4, default=Decimal(0), null=True, blank=True
    )

    note = models.TextField(null=True, blank=True, default="")

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')}, Stock {self.stock}, share {self.shares}, price {self.price}"


class StockPrice(BaseTimeStampModel):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
