import requests
import datetime
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse

from money import models


@login_required
def update_balance(request, account_id):
    account = models.Account.objects.get(pk=account_id)
    transactions = account.transaction_set.all().order_by("date", "-amount")

    sum = 0
    for transaction in transactions:
        sum += transaction.amount
        transaction.balance = sum
        transaction.save()
        account.last_transaction = transaction.date

    account.amount = sum
    account.last_update = datetime.datetime.now()
    account.save()

    stocks = (
        account.stocktransaction_set.all()
        .order_by("date", "-amount")
        .prefetch_related("stock")
    )

    stock_sum = defaultdict(int)

    for stock in stocks:
        stock_sum[stock.stock.id] += stock.shares
        stock.balance = stock_sum[stock.stock.id]
        stock.save()

    return JsonResponse({"success": True})


@login_required
def update_retailer_type(request):
    result = (
        models.Transaction.objects.values("type", "retailer__id")
        .annotate(count=Count("type"))
        .order_by("retailer__id", "count")
    )
    for retailer in result:
        if retailer["retailer__id"]:
            retailer_model = models.Retailer.objects.get(pk=retailer["retailer__id"])
            retailer_model.category = retailer["type"]
            retailer_model.type = models.RetailerType.ETC
            retailer_model.save()

    return JsonResponse({"success": True})


@login_required
def get_retailer_type(request, retailer_id):
    retailer = models.Retailer.objects.get(pk=retailer_id)
    return JsonResponse({"retailer_category": retailer.category})


@login_required
def update_related_transaction(request):
    if request.method == "POST":
        # Get the form data from the request.POST dictionary
        updated = {}
        for item, value in request.POST.items():
            if item.startswith("name_") and value:
                source_id = int(item[5:])
                target_id = int(value)

                source = models.Transaction.objects.get(id=source_id)
                target = models.Transaction.objects.get(id=target_id)

                if (
                    source.related_transaction is None
                    and target.related_transaction is None
                    and source.is_internal
                    and target.is_internal
                    and source_id != target_id
                ):
                    if abs(source.amount + target.amount) < 0.01:
                        source.related_transaction = target
                        target.related_transaction = source

                        target.save()
                        source.save()
                        updated[item] = value
        return JsonResponse(updated)


@login_required
def set_detail_required(request):
    objects = (
        models.Transaction.objects.filter(
            Q(type=models.TransactionCategory.DAILY_NECESSITY)
            | Q(type=models.TransactionCategory.GROCERY)
        )
        .filter(reviewed=False)
        .filter(requires_detail=False)
    )

    for obj in objects:
        obj.requires_detail = True
        obj.save()
    return JsonResponse({"success": True})


@login_required
def toggle_reviewed(request, transaction_id):
    transaction = models.Transaction.objects.get(pk=transaction_id)
    transaction.reviewed = not transaction.reviewed
    transaction.save()

    return JsonResponse({"success": True, "transaction_id": transaction_id})


def get_exchange_rate(request):
    headers = {"apikey": "FcfMFHmo63q1LeBD13Okk7rJjNrUQTXS"}
    response = requests.get(
        "https://api.apilayer.com/exchangerates_data/convert?to=KRW&from=USD&amount=5",
        headers=headers,
    )
    print(response)

    return JsonResponse(response)
