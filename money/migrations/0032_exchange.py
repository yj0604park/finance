# Generated by Django 4.1.8 on 2023-05-07 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("money", "0031_alter_transactiondetail_transaction"),
    ]

    operations = [
        migrations.CreateModel(
            name="Exchange",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("from_amount", models.FloatField()),
                ("to_amount", models.FloatField()),
                (
                    "from_currency",
                    models.CharField(
                        choices=[("KRW", "원화"), ("USD", "달러")], max_length=3
                    ),
                ),
                (
                    "to_currency",
                    models.CharField(
                        choices=[("KRW", "원화"), ("USD", "달러")], max_length=3
                    ),
                ),
                (
                    "from_transaction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exchange_from",
                        to="money.transaction",
                    ),
                ),
                (
                    "to_transaction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exchange_to",
                        to="money.transaction",
                    ),
                ),
            ],
        ),
    ]