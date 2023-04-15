from django.db import models
from django.urls import reverse


class Bank(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class AccountType(models.TextChoices):
    CHECKING_ACCOUNT = "CHECKING_ACCOUNT", "입출금"
    SAVINGS_ACCOUNT = "SAVINGS_ACCOUNT", "저금"
    INSTALLMENT_SAVING = "INSTALLMENT_SAVING", "적금"
    TIME_DEPOSIT = "TIME_DEPOSIT", "예금"
    CREDIT_CARD = "CREDIT_CARD", "신용카드"


class Account(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(
        max_length=30, choices=AccountType.choices, default=AccountType.CHECKING_ACCOUNT
    )
    amount = models.FloatField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)
    last_transaction = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.bank.name + ":" + self.name


class TransactionCategory(models.TextChoices):
    SERVICE = "SERVICE", "서비스"
    DAILY_NECESSITY = "DAILY_NECESSITY", "생필품"
    MEMBERSHIP = "MEMBERSHIP", "맴버쉽"
    GROCERY = "GROCERY", "식료품"
    EAT_OUT = "EAT_OUT", "외식"
    CLOTHING = "CLOTHING", "옷"
    PRESENT = "PRESENT", "선물"
    CAR = "CAR", "차/주유"
    HOUSING = "HOUSING", "집/월세"
    LEISURE = "LEISURE", "여가"
    MEDICAL = "MEDICAL", "의료비"
    PARENTING = "PARENTING", "육아"
    TRANSFER = "TRANSFER", "이체"
    INTEREST = "INTEREST", "이자"
    INCOME = "INCOME", "소득"
    ETC = "ETC", "ETC"


class UseFor(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    use_for = models.ForeignKey(
        UseFor, on_delete=models.SET_NULL, blank=True, null=True
    )
    amount = models.FloatField()
    balance = models.FloatField(null=True, blank=True)
    datetime = models.DateTimeField()
    note = models.TextField(null=True, blank=True)
    is_internal = models.BooleanField(default=False)
    requires_detail = models.BooleanField(default=False)

    type = models.CharField(
        max_length=30,
        choices=TransactionCategory.choices,
        default=TransactionCategory.ETC,
    )
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.datetime.strftime("%Y-%m-%d")} {self.account.name}: {self.use_for.name if self.use_for else None}'

    def get_absolute_url(self):
        return reverse("money:transaction_detail", kwargs={"pk": self.pk})


class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    note = models.CharField(max_length=40)
    amount = models.FloatField()
