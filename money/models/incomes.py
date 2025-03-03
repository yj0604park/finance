from django.db import models

from money.models.base import BaseCurrencyModel, BaseTimeStampModel, BaseURLModel
from money.models.transactions import Transaction


class Salary(BaseTimeStampModel, BaseURLModel, BaseCurrencyModel):
    gross_pay = models.DecimalField(max_digits=15, decimal_places=2)
    total_adjustment = models.DecimalField(max_digits=15, decimal_places=2)
    total_withheld = models.DecimalField(max_digits=15, decimal_places=2)
    total_deduction = models.DecimalField(max_digits=15, decimal_places=2)
    net_pay = models.DecimalField(max_digits=15, decimal_places=2)

    pay_detail = models.JSONField()
    adjustment_detail = models.JSONField()
    tax_detail = models.JSONField()
    deduction_detail = models.JSONField()

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}"


class W2(BaseTimeStampModel, BaseCurrencyModel):
    year = models.IntegerField()

    wages = models.DecimalField(max_digits=15, decimal_places=2)
    income_tax = models.DecimalField(max_digits=15, decimal_places=2)
    social_security_wages = models.DecimalField(max_digits=15, decimal_places=2)
    social_security_tax = models.DecimalField(max_digits=15, decimal_places=2)
    medicare_wages = models.DecimalField(max_digits=15, decimal_places=2)
    medicare_tax = models.DecimalField(max_digits=15, decimal_places=2)

    box_12 = models.JSONField(blank=True, null=True)
    box_14 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.date}"
