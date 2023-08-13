# Generated by Django 4.1.8 on 2023-08-12 22:07

from django.db import migrations
import django_choices_field.fields
import money.choices


class Migration(migrations.Migration):
    dependencies = [
        ("money", "0043_alter_account_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="currency",
            field=django_choices_field.fields.TextChoicesField(
                choices=[("KRW", "원화"), ("USD", "달러")],
                choices_enum=money.choices.CurrencyType,
                default="USD",
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="amountsnapshot",
            name="currency",
            field=django_choices_field.fields.TextChoicesField(
                choices=[("KRW", "원화"), ("USD", "달러")],
                choices_enum=money.choices.CurrencyType,
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="detailitem",
            name="category",
            field=django_choices_field.fields.TextChoicesField(
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
                    ("SEAFOOD", "해산물"),
                    ("INGREDIENT", "식재료"),
                    ("APPLIANCE", "가전"),
                    ("STATIONERY", "문구류"),
                    ("BATH", "욕실용품"),
                    ("BABY", "육아용품"),
                    ("COOKER", "주방용품"),
                    ("FOOD", "식품"),
                    ("CLOTHING", "의류"),
                    ("FUNITURE", "가구"),
                    ("SPORTING", "운동용품"),
                    ("UNK", "Unknown"),
                ],
                choices_enum=money.choices.DetailItemCategory,
                default="ETC",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="from_currency",
            field=django_choices_field.fields.TextChoicesField(
                choices=[("KRW", "원화"), ("USD", "달러")],
                choices_enum=money.choices.CurrencyType,
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="exchange",
            name="to_currency",
            field=django_choices_field.fields.TextChoicesField(
                choices=[("KRW", "원화"), ("USD", "달러")],
                choices_enum=money.choices.CurrencyType,
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="retailer",
            name="category",
            field=django_choices_field.fields.TextChoicesField(
                choices=[
                    ("SERVICE", "서비스"),
                    ("DAILY_NECESSITY", "생필품"),
                    ("MEMBERSHIP", "맴버쉽"),
                    ("GROCERY", "식료품"),
                    ("EAT_OUT", "외식"),
                    ("CLOTHING", "옷"),
                    ("PRESENT", "선물"),
                    ("CAR", "차/주유"),
                    ("HOUSING", "집/월세"),
                    ("LEISURE", "여가"),
                    ("MEDICAL", "의료비"),
                    ("PARENTING", "육아"),
                    ("TRANSFER", "이체"),
                    ("INTEREST", "이자"),
                    ("INCOME", "소득"),
                    ("ETC", "ETC"),
                    ("STOCK", "주식"),
                    ("CASH", "현금"),
                ],
                choices_enum=money.choices.TransactionCategory,
                default="ETC",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="retailer",
            name="type",
            field=django_choices_field.fields.TextChoicesField(
                choices=[
                    ("ETC", "Etc"),
                    ("STORE", "Store"),
                    ("PERSON", "Person"),
                    ("BANK", "Bank"),
                    ("SERVICE", "Service"),
                    ("INCOME", "Income"),
                    ("RESTAURANT", "Restaurant"),
                ],
                choices_enum=money.choices.RetailerType,
                default="ETC",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="stock",
            name="currency",
            field=django_choices_field.fields.TextChoicesField(
                choices=[("KRW", "원화"), ("USD", "달러")],
                choices_enum=money.choices.CurrencyType,
                default="USD",
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="type",
            field=django_choices_field.fields.TextChoicesField(
                choices=[
                    ("SERVICE", "서비스"),
                    ("DAILY_NECESSITY", "생필품"),
                    ("MEMBERSHIP", "맴버쉽"),
                    ("GROCERY", "식료품"),
                    ("EAT_OUT", "외식"),
                    ("CLOTHING", "옷"),
                    ("PRESENT", "선물"),
                    ("CAR", "차/주유"),
                    ("HOUSING", "집/월세"),
                    ("LEISURE", "여가"),
                    ("MEDICAL", "의료비"),
                    ("PARENTING", "육아"),
                    ("TRANSFER", "이체"),
                    ("INTEREST", "이자"),
                    ("INCOME", "소득"),
                    ("ETC", "ETC"),
                    ("STOCK", "주식"),
                    ("CASH", "현금"),
                ],
                choices_enum=money.choices.TransactionCategory,
                default="ETC",
                max_length=30,
            ),
        ),
    ]
