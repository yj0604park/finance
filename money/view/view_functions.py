import datetime
import json
from collections import defaultdict

import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render

from money import choices, forms, helper, models


def update_balance(request, account_id):
    account = models.Account.objects.get(pk=account_id)
    transactions = account.transaction_set.all().order_by("date", "-amount")

    total = 0
    first = True
    for transaction in transactions:
        if first:
            account.first_transaction = transaction.date
            first = False
        total += transaction.amount
        if abs(total) < 0.01:
            total = 0
        transaction.balance = total
        transaction.save()
        account.last_transaction = transaction.date

    account.amount = total
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
    # update retailer type based on the transaction type frequency
    result = (
        models.Transaction.objects.values("type", "retailer__id")
        .annotate(count=Count("type"))
        .order_by("retailer__id", "count")
    )
    for retailer in result:
        if retailer["retailer__id"]:
            retailer_model = models.Retailer.objects.get(pk=retailer["retailer__id"])
            retailer_model.category = retailer["type"]
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

                source: models.Transaction = models.Transaction.objects.get(
                    id=source_id
                )
                target: models.Transaction = models.Transaction.objects.get(
                    id=target_id
                )

                if source.account.currency == target.account.currency:
                    if (
                        source.related_transaction is None
                        and target.related_transaction is None
                        and source.is_internal
                        and target.is_internal
                        and source_id != target_id
                        and source.account.pk != target.account.pk
                    ):
                        if abs(source.amount + target.amount) < 0.01:
                            source.related_transaction = target
                            target.related_transaction = source

                            target.save()
                            source.save()
                            updated[item] = value
                else:
                    # 환전
                    if (
                        source.date == target.date
                        and source.related_transaction is None
                        and target.related_transaction is None
                        and source.is_internal
                        and target.is_internal
                        and source_id != target_id
                        and source.account.pk != target.account.pk
                        and source.amount * target.amount < 0
                    ):
                        if source.amount > 0:
                            # source should has minus amount
                            temp = source
                            source = target
                            target = temp

                        if source.account.currency == choices.CurrencyType.KRW:
                            ratio = source.amount / target.amount
                        else:
                            ratio = target.amount / source.amount

                        ratio = round(-ratio, 2)

                        if ratio > 1600 or ratio < 1000:
                            continue

                        exchange = models.Exchange(
                            date=source.date,
                            from_transaction=source,
                            to_transaction=target,
                            from_amount=source.amount,
                            to_amount=target.amount,
                            from_currency=source.account.currency,
                            to_currency=target.account.currency,
                            ratio_per_krw=ratio,
                        )
                        exchange.save()

                        source.related_transaction = target
                        target.related_transaction = source

                        target.save()
                        source.save()
                        updated[item] = value

        return JsonResponse(updated)
    return HttpResponseNotAllowed(permitted_methods=["POST"])


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


@login_required
def get_items_for_category(request: HttpRequest):
    if request.method == "POST":
        post_data = json.loads(request.body.decode())
        item_list = models.DetailItem.objects.filter(
            category=post_data["category"]
        ).values("pk", "name")
        item_list = sorted(list(item_list), key=lambda x: x["name"].lower())

        return JsonResponse({"result": item_list})
    return HttpResponseNotAllowed(permitted_methods=["POST"])


@login_required
def update_related_transaction_for_amazon(request: HttpRequest):
    if request.method == "POST":
        post_data = json.loads(request.body.decode())
        transaction = models.Transaction.objects.get(pk=post_data["transaction_id"])
        order = models.AmazonOrder.objects.get(pk=post_data["order_id"])
        order.transaction = transaction
        order.save()
        return JsonResponse(
            {
                "success": True,
                "transaction": transaction.__str__(),
                "amount": transaction.amount,
            }
        )

    return HttpResponseNotAllowed(permitted_methods=["POST"])


@login_required
def get_exchange_rate(request):
    headers = {"apikey": "FcfMFHmo63q1LeBD13Okk7rJjNrUQTXS"}
    response = requests.get(
        "https://api.apilayer.com/exchangerates_data/convert?to=KRW&from=USD&amount=5",
        headers=headers,
    )
    print(response)

    return JsonResponse(response)


@login_required
def create_daily_snapshot(request):
    helper.create_daily_snapshot()
    return JsonResponse({"success": True})


@login_required
# trunk-ignore(pylint/W0613)
def get_stock_snapshot(request):
    stock_snapshot = helper.get_stock_snapshot()

    return JsonResponse({"data": stock_snapshot})


@login_required
def filter_retailer(request):
    keyword = request.GET.get("keyword")
    filtered = models.Retailer.objects.filter(name__icontains=keyword)

    filtered_obj_list = [
        {"name": obj.name, "id": obj.pk, "str": str(obj)} for obj in filtered
    ]
    return JsonResponse({"filtered_list": filtered_obj_list})


@login_required
def file_upload(request):
    if request.method == "POST":
        print("Post")
        form = forms.TransactionFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
    else:
        form = forms.TransactionFileForm()
    print("hi")
    return render(request, "file/upload.html", {"form": form})


@login_required
def get_end_month_balance(request):
    accounts = models.Account.objects.filter(is_active=True)
    end_month_balances = []

    year = "2024"

    for account in accounts:
        account_balances = []
        for month in range(1, 13):
            last_transaction = (
                account.transaction_set.filter(date__year=year, date__month=month)
                .order_by("date", "-amount")
                .last()
            )

            if last_transaction is None:
                continue

            account_balances.append(
                {
                    "month": month,
                    "balance": last_transaction.balance,
                    "transaction_id": last_transaction.id,
                }
            )

        end_month_balances.append(
            {
                "account_id": account.id,
                "account_name": account.name,
                "balance": account_balances,
            }
        )

    return JsonResponse({"end_month_balances": end_month_balances})
