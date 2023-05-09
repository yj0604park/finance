import json
from money import models
import re


def run():
    kakao_retailer = models.Retailer.objects.get(name="카카오뱅크")

    saving_account_pattern = re.compile("(\d{4})")

    for transaction in models.Transaction.objects.filter(
        account_id=9, reviewed=False, type=models.TransactionCategory.ETC
    ):
        data = json.loads(transaction.note)

        retailer = data["retailer"].strip()

        if data["retailer"] != retailer:
            data["retailer"] = retailer
            transaction.note = json.dumps(
                data,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
            transaction.save()

        if (
            ("적금" in retailer and "신규" not in retailer)
            or ("적금" in retailer and "해지" in retailer)
            or retailer == "세이프박스"
        ):
            if "적금" in retailer:
                print(transaction)
                print(retailer)
                account_number = saving_account_pattern.search(retailer).group(1)
                account_name = f"카카오 적금 ({account_number})"
            elif retailer == "세이프박스":
                account_name = "세이프박스"
            else:
                raise Exception(f"Unknown 적금 {retailer}")

            if models.Account.objects.filter(name=account_name).count() == 0:
                models.Account(
                    name=account_name,
                    bank_id=5,
                    type=models.AccountType.INSTALLMENT_SAVING,
                    currency=models.CurrencyType.KRW,
                ).save()
            account = models.Account.objects.get(name=account_name)

            related = models.Transaction(
                account=account,
                amount=-transaction.amount,
                date=transaction.date,
                note=transaction.note,
                is_internal=True,
                type=models.TransactionCategory.TRANSFER,
                reviewed=True,
                related_transaction=transaction,
            )

            related.save()

            transaction.related_transaction = related
            transaction.is_internal = True
            transaction.type = models.TransactionCategory.TRANSFER
            transaction.reviewed = True

            transaction.save()

        if "입출금통장 이자" in retailer or "세이프박스 이자" in retailer:
            transaction.type = models.TransactionCategory.INTEREST
            transaction.retailer = kakao_retailer
            transaction.reviewed = True
            transaction.save()
