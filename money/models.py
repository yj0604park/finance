from django.db import models
from django.urls import reverse
from money.choices import (
    AccountType,
    CurrencyType,
    DetailItemCategory,
    RetailerType,
    TransactionCategory,
)


class Bank(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Account(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(
        max_length=30, choices=AccountType.choices, default=AccountType.CHECKING_ACCOUNT
    )
    amount = models.FloatField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)
    last_transaction = models.DateField(null=True, blank=True)
    first_transaction = models.DateField(null=True, blank=True)
    first_added = models.BooleanField(default=False)
    currency = models.CharField(
        max_length=3, choices=CurrencyType.choices, default=CurrencyType.USD
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Retailer(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(
        max_length=20, choices=RetailerType.choices, default=RetailerType.ETC
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


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    retailer = models.ForeignKey(
        Retailer, on_delete=models.SET_NULL, blank=True, null=True
    )
    amount = models.FloatField()
    balance = models.FloatField(null=True, blank=True)
    date = models.DateField()
    note = models.TextField(null=True, blank=True)
    is_internal = models.BooleanField(default=False)
    requires_detail = models.BooleanField(default=False)

    type = models.CharField(
        max_length=30,
        choices=TransactionCategory.choices,
        default=TransactionCategory.ETC,
    )
    reviewed = models.BooleanField(default=False)

    related_transaction = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )

    def get_absolute_url(self):
        return reverse("money:transaction_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return (
            f'{self.id} {self.date.strftime("%Y-%m-%d")} '
            + f"{self.account.name}: "
            + f"{self.retailer.name if self.retailer else None}"
        )


class Stock(models.Model):
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=10, null=True, blank=True)
    currency = models.CharField(
        max_length=3, choices=CurrencyType.choices, default=CurrencyType.USD
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
        Transaction, on_delete=models.SET_NULL, null=True, blank=True
    )

    price = models.FloatField()
    shares = models.FloatField()
    amount = models.FloatField()
    balance = models.FloatField(default=0, null=True, blank=True)

    note = models.TextField(null=True, blank=True, default="")

    def get_absolute_url(self):
        return reverse("money:stock_transaction_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')}, Stock {self.stock.id}, share {self.shares}, price {self.price}"


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.FloatField()


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


class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item = models.ForeignKey(DetailItem, on_delete=models.CASCADE)

    note = models.CharField(max_length=40, blank=True, null=True)
    amount = models.FloatField()
    count = models.FloatField(default=1)


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
    from_currency = models.CharField(max_length=3, choices=CurrencyType.choices)
    to_currency = models.CharField(max_length=3, choices=CurrencyType.choices)
    ratio_per_krw = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.date}: {self.ratio_per_krw}"


class AmountSnapshot(models.Model):
    date = models.DateField()
    currency = models.CharField(max_length=3, choices=CurrencyType.choices)
    amount = models.FloatField()
    summary = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.date}: {self.currency}"
