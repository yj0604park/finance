# Generated by Django 4.1.8 on 2023-04-21 00:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("money", "0007_rename_usefor_retailer"),
    ]

    operations = [
        migrations.RenameField(
            model_name="transaction",
            old_name="use_for",
            new_name="retailer",
        ),
    ]
