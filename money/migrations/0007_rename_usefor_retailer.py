# Generated by Django 4.1.8 on 2023-04-21 00:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("money", "0006_transaction_reviewed_alter_transaction_type"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UseFor",
            new_name="Retailer",
        ),
    ]
