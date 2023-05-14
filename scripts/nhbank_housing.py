from money import models


def run():
    with open("data/nhbank_housing.txt") as f:
        for line in f:
            line = line.strip()

            if line:
                obj = models.Transaction(
                    account_id=149,
                    amount=100000,
                    date=line,
                    is_internal=True,
                    type=models.TransactionCategory.TRANSFER,
                )
                obj.save()
