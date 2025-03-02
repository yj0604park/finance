from django.db import models
from django.urls import reverse
from django_choices_field import TextChoicesField

from money.choices import CurrencyType, ExchangeType
from money.models.accounts import Account
from money.models.transaction import Transaction


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


class Salary(models.Model):
    date = models.DateField()
    gross_pay = models.FloatField()
    total_adjustment = models.FloatField()
    total_withheld = models.FloatField()
    total_deduction = models.FloatField()
    net_pay = models.FloatField()

    pay_detail = models.JSONField()
    adjustment_detail = models.JSONField()
    tax_detail = models.JSONField()
    deduction_detail = models.JSONField()

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("money:salary_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.date}"


class AmazonOrder(models.Model):
    date = models.DateField()
    item = models.TextField()
    is_returned = models.BooleanField(default=False)
    transaction = models.ForeignKey(
        Transaction, null=True, blank=True, on_delete=models.SET_NULL
    )
    return_transaction = models.ForeignKey(
        Transaction,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="returned_order",
    )

    class Meta:
        ordering = ["date"]

    def get_absolute_url(self):
        return reverse("money:amazon_order_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} {self.item}"


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


class W2(models.Model):
    date = models.DateField()
    year = models.IntegerField()
    wages = models.DecimalField(max_digits=10, decimal_places=2)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2)
    social_security_wages = models.DecimalField(max_digits=10, decimal_places=2)
    social_security_tax = models.DecimalField(max_digits=10, decimal_places=2)
    medicare_wages = models.DecimalField(max_digits=10, decimal_places=2)
    medicare_tax = models.DecimalField(max_digits=10, decimal_places=2)
    box_12 = models.JSONField(blank=True, null=True)
    box_14 = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.date}"
