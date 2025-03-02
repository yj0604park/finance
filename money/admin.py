from django import forms
from django.contrib import admin

from money.models import models
from money.models.accounts import Account, Bank, AmountSnapshot


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "bank", "currency", "is_active", "first_added"]
    list_filter = ["is_active", "bank", "first_added"]


@admin.register(AmountSnapshot)
class AmountSnapshotAdmin(admin.ModelAdmin):
    date_hierarchy = "date"


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
    raw_id_fields = ("related_transaction", "account")
    list_filter = ["account", "type"]

    def account_name(self, obj):
        return obj.account.name

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("account", "retailer")


@admin.register(models.Retailer)
class RetailerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type", "category"]
    list_filter = ["type", "category"]


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

    list_display = ("id", "item", "amount", "count")


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
    list_display = ("id", "ticker", "name", "currency")


@admin.register(models.StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ("id", "stock", "date", "price")


@admin.register(models.StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    raw_id_fields = ("related_transaction",)


@admin.register(models.AmazonOrder)
class AmazonOrderAdmin(admin.ModelAdmin):
    list_display = ["id", "item", "date", "is_returned", "transaction"]
    raw_id_fields = ("transaction", "return_transaction")
    date_hierarchy = "date"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "transaction",
                "return_transaction",
                "transaction__account",
                "transaction__retailer",
                "return_transaction__account",
            )
        )


@admin.register(models.Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "id", "date", "ratio_per_krw", "exchange_type"]
    list_filter = ["exchange_type"]
    raw_id_fields = ("from_transaction", "to_transaction")
    date_hierarchy = "date"


@admin.register(models.TransactionFile)
class TransactionFile(admin.ModelAdmin):
    list_display = ["id", "file", "date"]
    date_hierarchy = "date"


@admin.register(models.W2)
class W2Admin(admin.ModelAdmin):
    list_display = ["id", "year", "date"]
    date_hierarchy = "date"
    list_filter = ["year"]
    search_fields = ["year"]
