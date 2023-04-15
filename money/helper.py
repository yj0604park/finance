import datetime

from django.http import HttpResponse

from money import models


def get_transaction_chart_data(transaction_list, recalculate=False):
    chart_dict = []
    sum = 0
    for transaction in transaction_list:
        sum += transaction.amount
        chart_dict.append(
            {
                "x": transaction.datetime.strftime("%Y-%m-%d"),
                "y": transaction.balance if not recalculate else sum,
            }
        )
    return chart_dict


def updateBalance(request, account_id):
    account = models.Account.objects.get(pk=account_id)
    transactions = account.transaction_set.all().order_by("datetime", "-amount")

    sum = 0
    for transaction in transactions:
        sum += transaction.amount
        transaction.balance = sum
        transaction.save()
        account.last_transaction = transaction.datetime

    account.amount = sum
    account.last_update = datetime.datetime.now()
    account.save()

    html = "<html><body>Updated</body></html>"
    return HttpResponse(html)
