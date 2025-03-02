from django.db import models
from django.urls import reverse

from money.models.transactions import Transaction


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
