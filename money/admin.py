from django.contrib import admin
from money import models


@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "bank"]


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["pk", "datetime", "account_name", "retailer"]
    raw_id_fields = ("related_transaction",)

    def account_name(self, obj):
        return obj.account.name

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("account", "retailer")


@admin.register(models.Retailer)
class RetailerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DetailItem)
class DetailItemAdmin(admin.ModelAdmin):
    pass


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
                .order_by("datetime")
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
