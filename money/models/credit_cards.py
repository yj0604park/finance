from django.db import models


class CreditCard(models.Model):
    """Credit card info with benefits linked to an Account."""

    account = models.OneToOneField(
        "Account", on_delete=models.CASCADE, related_name="credit_card",
        limit_choices_to={"type": "CREDIT_CARD"},
    )
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["account__name"]

    def __str__(self):
        return f"{self.account.name} (Credit Card)"


class CreditCardBenefit(models.Model):
    """Individual benefit/perk for a credit card."""

    class BenefitCategory(models.TextChoices):
        CASHBACK = "CASHBACK", "캐시백"
        POINTS = "POINTS", "포인트"
        DISCOUNT = "DISCOUNT", "할인"
        MILEAGE = "MILEAGE", "마일리지"
        OTHER = "OTHER", "기타"

    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name="benefits")
    category = models.CharField(max_length=20, choices=BenefitCategory.choices, default=BenefitCategory.DISCOUNT)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Percentage (e.g. 5.00 = 5%)")
    cap_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, help_text="Monthly cap in KRW")
    conditions = models.TextField(blank=True, default="", help_text="Conditions to qualify")

    class Meta:
        ordering = ["-rate"]

    def __str__(self):
        return f"{self.credit_card.account.name} - {self.title}"
