# Generated by Django 4.1.8 on 2023-04-24 09:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("money", "0014_detailitem_transactiondetail_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transactiondetail",
            name="note",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
