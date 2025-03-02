from rest_framework import serializers

from money.models.accounts import Bank


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ["name"]
