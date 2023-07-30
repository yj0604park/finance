import json

from money import models


def run():
    for transaction in models.Transaction.objects.filter(
        account_id=8, reviewed=False, type=models.TransactionCategory.ETC
    ):
        note = json.loads(transaction.note)

        if note["retailer"] == "유민주":
            retailer = models.Retailer.objects.get(name="Minjoo Yoo")
            transaction.type = models.TransactionCategory.TRANSFER
            transaction.retailer = retailer
            transaction.reviewed = True
            transaction.save()

        if (
            note["retailer"] == "급여"
            or note["retailer"] == "박윤재"
            or note["retailer"] == "KB카드출금"
            or note["retailer"] == "카드대금결제"
            or note["retailer"] == "신한카드"
            or note["retailer"] == "20600904025240"
            or note["retailer"] == "토스 박윤재"
        ):
            transaction.type = models.TransactionCategory.TRANSFER
            transaction.is_internal = True
            transaction.save()

        if (
            "티플러스" in note["retailer"]
            or "KT98729577" in note["retailer"]
            or "KT통신요금" in note["retailer"]
        ):
            retailer = models.Retailer.objects.get(name="Communication Cost")
            transaction.retailer = retailer
            transaction.type = models.TransactionCategory.SERVICE
            transaction.reviewed = True
            transaction.save()

        if "삼성" in note["retailer"] and "002건" in note["retailer"]:
            retailer = models.Retailer.objects.get(name="Life Insurance")
            transaction.retailer = retailer
            transaction.type = models.TransactionCategory.SERVICE
            transaction.reviewed = True
            transaction.save()

        if "이자세금" in note["retailer"]:
            retailer = models.Retailer.objects.get(name="KB Bank")
            transaction.retailer = retailer
            transaction.type = models.TransactionCategory.INTEREST
            transaction.reviewed = True
            transaction.save()

        if note["retailer"] == "신림건영3차" or note["retailer"] == "서울도시가스":
            retailer = models.Retailer.objects.get(name=note["retailer"])
            transaction.retailer = retailer
            transaction.type = models.TransactionCategory.HOUSING
            transaction.reviewed = True
            transaction.save()
