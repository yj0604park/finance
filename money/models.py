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
    STOCK = "STOCK", "주식"


class CurrencyType(models.TextChoices):
    KRW = "KRW", "원화"
    USD = "USD", "달러"


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
    currency = models.CharField(
        max_length=3, choices=CurrencyType.choices, default=CurrencyType.USD
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


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


class RetailerType(models.TextChoices):
    ETC = "ETC"
    STORE = "STORE"
    PERSON = "PERSON"
    BANK = "BANK"
    SERVICE = "SERVICE"


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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


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

    def __str__(self):
        return f'{self.id} {self.date.strftime("%Y-%m-%d")} {self.account.name}: {self.retailer.name if self.retailer else None}'

    def get_absolute_url(self):
        return reverse("money:transaction_detail", kwargs={"pk": self.pk})


class Stock(models.Model):
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=10, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("money:stock_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.ticker}: {self.name}"

    class Meta:
        ordering = ["ticker"]


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

    note = models.TextField(null=True, blank=True, default="")

    def get_absolute_url(self):
        return reverse("money:stock_transaction_detail", kwargs={"pk": self.pk})


class DetailItemCategory(models.TextChoices):
    ETC = "ETC", "ETC"
    FRUIT = "FRUIT", "과일"
    ALCOHOL = "ALCOHOL", "주류"
    DRINK = "DRINK", "음료"
    SAUCE = "SAUCE", "소스"
    MEAT = "MEAT", "육류"
    VEGETABLE = "VEGETABLE", "채소"
    DAIRY = "DAIRY", "유제품"
    WRAP = "WRAP", "포장지"
    SNACK = "SNACK", "스낵"
    NOODLE = "NOODLE", "면"
    BREAD = "BREAD", "빵"
    DRUG = "DRUG", "약"
    TAX = "TAX", "TAX"
    SEAFOOD = "SEAFOOD", "해산물"
    INGREDIENT = "INGREDIENT", "식재료"
    APPLIANCE = "APPLIANCE", "가전"
    STATIONERY = "STATIONERY", "문구류"
    BATH = "BATH", "욕실용품"
    BABY = "BABY", "육아용품"
    COOKER = "COOKER", "주방용품"
    FOOD = "FOOD", "식품"
    CLOTHING = "CLOTHING", "의류"
    UNK = "UNK", "Unknown"


class DetailItem(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(
        max_length=10,
        choices=DetailItemCategory.choices,
        default=DetailItemCategory.ETC,
    )

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f"{self.date}"

    def get_absolute_url(self):
        return reverse("money:salary_detail", kwargs={"pk": self.pk})


class AmazonOrder(models.Model):
    date = models.DateField()
    item = models.TextField()
    is_returned = models.BooleanField(default=False)
    transaction = models.ForeignKey(
        Transaction, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} {self.item}"

    def get_absolute_url(self):
        return reverse("money:amazon_order_detail", kwargs={"pk": self.pk})


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
