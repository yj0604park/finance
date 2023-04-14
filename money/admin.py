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
    pass


@admin.register(models.UseFor)
class UseFor(admin.ModelAdmin):
    pass
