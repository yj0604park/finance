from django.contrib import admin
from django import forms
from money import models


@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "bank", "currency"]


class TransactionAdminForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sorted_choices = models.Retailer.objects.all().order_by("name").values("name")
        self.fields["retailer"].choices = sorted_choices


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "date",
        "account_name",
        "amount",
        "retailer",
        "type",
        "reviewed",
    ]
    raw_id_fields = ("related_transaction",)
    list_filter = ["account"]

    def account_name(self, obj):
        return obj.account.name

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("account", "retailer")


@admin.register(models.Retailer)
class RetailerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DetailItem)
class DetailItemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category"]
    list_filter = ["category"]

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "category":
            # Get the existing choices.
            choices = models.DetailItemCategory.choices

            # Sort the choices in lexicographic order.
            kwargs["choices"] = sorted(choices, key=lambda x: x[1])

        return super().formfield_for_choice_field(db_field, request, **kwargs)


@admin.register(models.TransactionDetail)
class TransactionDetailAdmin(admin.ModelAdmin):
    raw_id_fields = ("transaction",)


@admin.register(models.Salary)
class SalaryAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "transaction":
            kwargs["queryset"] = (
                models.Transaction.objects.filter(
                    type=models.TransactionCategory.INCOME
                )
                .prefetch_related("account", "retailer")
                .order_by("date")
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    pass
