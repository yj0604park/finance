# Generated by Django 4.1.8 on 2023-05-03 04:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("money", "0022_stock_stocktransaction"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="stock",
            options={"ordering": ["ticker"]},
        ),
        migrations.AddField(
            model_name="detailitem",
            name="category",
            field=models.CharField(
                choices=[
                    ("ETC", "ETC"),
                    ("FRUIT", "과일"),
                    ("ALCOHOL", "주류"),
                    ("DRINK", "음료"),
                    ("SAUCE", "소스"),
                    ("MEAT", "육류"),
                    ("VEGETABLE", "채소"),
                    ("DAIRY", "유제품"),
                    ("WRAP", "포장지"),
                    ("SNACK", "스낵"),
                    ("NOODLE", "면"),
                    ("BREAD", "빵"),
                    ("DRUG", "약"),
                    ("TAX", "TAX"),
                ],
                default="ETC",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="retailer",
            name="type",
            field=models.CharField(
                choices=[
                    ("ETC", "Etc"),
                    ("STORE", "Store"),
                    ("PERSON", "Person"),
                    ("BANK", "Bank"),
                    ("SERVICE", "Service"),
                ],
                default="ETC",
                max_length=20,
            ),
        ),
    ]
