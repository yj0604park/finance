from django.db import models
from django.urls import reverse
from django_choices_field import TextChoicesField

from money.models.transactions import Transaction


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
