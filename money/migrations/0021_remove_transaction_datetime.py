# Generated by Django 4.1.8 on 2023-05-02 10:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("money", "0020_alter_retailer_options_transaction_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="datetime",
        ),
    ]