# Generated by Django 4.1.8 on 2023-05-03 08:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("money", "0023_alter_stock_options_detailitem_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transactiondetail",
            name="count",
            field=models.FloatField(default=1),
        ),
    ]
