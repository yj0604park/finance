from collections import defaultdict

from django.db import models
from django.urls import reverse
from django_choices_field import TextChoicesField

from money.choices import (
    AccountType,
    CurrencyType,
    DetailItemCategory,
    ExchangeType,
    RetailerType,
    TransactionCategory,
)


class Account(models.Model):
    """
    Model for a bank account.
    """

    bank = models.ForeignKey("Bank", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_collation="C")
    alias = models.CharField(max_length=200, blank=True, null=True)
    type = TextChoicesField(
        choices_enum=AccountType, default=AccountType.CHECKING_ACCOUNT
    )
    amount = models.FloatField(default=0)
    amount_int = models.BigIntegerField(default=0)

    last_update = models.DateTimeField(null=True, blank=True)
    last_transaction = models.DateField(null=True, blank=True)
    first_transaction = models.DateField(null=True, blank=True)
    first_added = models.BooleanField(default=False)
    currency = TextChoicesField(
        max_length=3, choices_enum=CurrencyType, default=CurrencyType.USD
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def account_type(self):
        return self.type


class Bank(models.Model):
    """
    Model for a bank.
    """

    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def balance(self):
        sum_dict = defaultdict(float)

        for account in Account.objects.filter(bank=self):
            sum_dict[account.currency] += account.amount
        return sum_dict


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
        return f"{self.date.strftime('%Y-%m-%d')}, Stock {self.stock.pk}, share {self.shares}, price {self.price}"


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.FloatField()


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
    from_currency = TextChoicesField(max_length=3, choices_enum=CurrencyType)
    to_currency = TextChoicesField(max_length=3, choices_enum=CurrencyType)
    ratio_per_krw = models.FloatField(null=True, blank=True)
    exchange_type = TextChoicesField(
        max_length=10, choices_enum=ExchangeType, default=ExchangeType.ETC
    )

    def __str__(self) -> str:
        return f"{self.date}: {self.ratio_per_krw}"


class AmountSnapshot(models.Model):
    date = models.DateField()
    currency = TextChoicesField(max_length=3, choices_enum=CurrencyType)
    amount = models.FloatField()
    summary = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.date}: {self.currency}"


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
