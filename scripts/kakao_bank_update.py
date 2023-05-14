import json
from money import models, choices
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
            or retailer == "저금통"
        ):
            if "적금" in retailer:
                print(transaction)
                print(retailer)
                account_number = saving_account_pattern.search(retailer).group(1)
                account_name = f"카카오 적금 ({account_number})"
            elif retailer == "세이프박스":
                account_name = "세이프박스"
            elif retailer == "저금통":
                account_name = "저금통"
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

        elif "입출금통장 이자" in retailer or "세이프박스 이자" in retailer:
            transaction.type = models.TransactionCategory.INTEREST
            transaction.retailer = kakao_retailer
            transaction.reviewed = True
            transaction.save()

        elif (
            data["note"] == "계좌간자동이체"
            or ("적금" in retailer and "신규" in retailer)
            or (retailer == "박윤재" and data["note"] == "일반이체")
        ):
            transaction.type = choices.TransactionCategory.TRANSFER
            transaction.is_internal = True
            transaction.save()

        elif "동행복권" in retailer or retailer == "Amazon_AWS" or "aws" in retailer:
            if "동행복권" in retailer:
                retailer_object = models.Retailer.objects.get(name="로또")
            if "Amazon" in retailer:
                retailer_object = models.Retailer.objects.get(name="Amazon AWS")
            transaction.retailer = retailer_object
            transaction.reviewed = True
            transaction.type = choices.TransactionCategory.LEISURE
            transaction.save()

        elif retailer == "대출이자" or retailer == "카카오뱅크 캐시백지급":
            retailer_object = models.Retailer.objects.get(name="카카오뱅크")
            transaction.retailer = retailer_object
            transaction.reviewed = True
            transaction.type = choices.TransactionCategory.INTEREST
            transaction.save()

        elif retailer == "유민주":
            retailer_object = models.Retailer.objects.get(name="Minjoo Yoo")
            transaction.retailer = retailer_object
            transaction.reviewed = True
            transaction.type = choices.TransactionCategory.TRANSFER
            transaction.save()
        elif retailer in ("이현영", "박형준"):
            retailer_object = models.Retailer.objects.get(name="가족")
            transaction.retailer = retailer_object
            transaction.reviewed = True
            transaction.type = choices.TransactionCategory.TRANSFER
            transaction.save()

        elif retailer in (
            "전성빈",
            "김혜인",
            "김호영",
            "손동희",
            "송광호",
            "서장혁",
            "구한준",
            "이재준",
            "김동완",
            "길태호",
            "정창용",
            "하소정",
            "권수용",
            "토스 김호영",
            "토스 하소정",
            "토스_현명욱",
            "간편이체(박상준)",
            "안종찬",
        ):
            retailer_object = models.Retailer.objects.get(name="친구")
            transaction.retailer = retailer_object
            transaction.reviewed = True
            transaction.type = choices.TransactionCategory.TRANSFER
            transaction.save()

        elif retailer == "ATM출금":
            transaction.reviewed = True
            transaction.type = choices.TransactionCategory.CASH
            transaction.save()

        elif "코인원" in retailer:
            retailer_object = models.Retailer.objects.get(name="투자")
            transaction.retailer = retailer_object
            transaction.reviewed = True
            transaction.type = choices.TransactionCategory.STOCK
            transaction.save()
