from django.db import models
from django.urls import reverse

from money.choices import CurrencyType


class BaseTimeStampModel(models.Model):
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseAmountModel(models.Model):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    amount_int = models.BigIntegerField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.amount_int = int(float(self.amount) * 100)
        super().save(*args, **kwargs)


class BaseURLModel(models.Model):
    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse(f"money:{self._meta.model_name}_detail", kwargs={"pk": self.pk})


class BaseCurrencyModel(models.Model):
    currency = models.CharField(
        max_length=3,
        choices=CurrencyType.choices,
        default=CurrencyType.USD,
    )

    class Meta:
        abstract = True
