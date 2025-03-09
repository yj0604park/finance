from django.db import models
from django.urls import reverse
from django_choices_field import TextChoicesField

from money.choices import CurrencyType


class BaseTimeStampModel(models.Model):
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseAmountModel(models.Model):
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        abstract = True


class BaseURLModel(models.Model):
    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse(f"money:{self._meta.model_name}_detail", kwargs={"pk": self.pk})


class BaseCurrencyModel(models.Model):
    currency = TextChoicesField(
        max_length=3, choices_enum=CurrencyType, default=CurrencyType.USD
    )

    class Meta:
        abstract = True
