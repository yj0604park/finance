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
    list_display = ["pk", "datetime", "account_name", "use_for"]

    def account_name(self, obj):
        return obj.account.name

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("account", "use_for")


@admin.register(models.UseFor)
class UseFor(admin.ModelAdmin):
    pass
