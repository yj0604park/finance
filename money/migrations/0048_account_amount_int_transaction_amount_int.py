# Generated by Django 4.1.8 on 2024-04-07 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("money", "0047_alter_stocktransaction_related_transaction"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="amount_int",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="transaction",
            name="amount_int",
            field=models.IntegerField(default=0),
        ),
    ]