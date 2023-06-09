# Generated by Django 4.1.8 on 2023-05-13 08:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("money", "0034_alter_stocktransaction_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="type",
            field=models.CharField(
                choices=[
                    ("CHECKING_ACCOUNT", "입출금"),
                    ("SAVINGS_ACCOUNT", "저금"),
                    ("INSTALLMENT_SAVING", "적금"),
                    ("TIME_DEPOSIT", "예금"),
                    ("CREDIT_CARD", "신용카드"),
                    ("STOCK", "주식"),
                    ("LOAN", "대출"),
                ],
                default="CHECKING_ACCOUNT",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="retailer",
            name="category",
            field=models.CharField(
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
                default="ETC",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="type",
            field=models.CharField(
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
                default="ETC",
                max_length=30,
            ),
        ),
    ]
