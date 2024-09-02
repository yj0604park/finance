import json

from money import models

WithDrawIndex = 4
DepositIndex = 5
BalanceIndex = 6


def run():
    with open("", encoding="utf-8") as f:  # update file name
        # 직장인우대통장
        # account = models.Account.objects.get(pk=8)

        for line in f:
            data = line.split("\t")
            print(data)

            balance = data[BalanceIndex].strip().replace(",", "")

            parse_data = {
                "date": data[0].replace(".", "-")[:10],
                "note": json.dumps(
                    {
                        "type": data[1].strip().replace(" ", ""),
                        "retailer": data[2].strip().replace(" ", ""),
                        "note": "",
                        "balance": float(balance),
                    },
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=False,
                ),
                "amount": (
                    -float(data[WithDrawIndex].strip().replace(",", ""))
                    if float(data[WithDrawIndex].strip().replace(",", ""))
                    else float(data[DepositIndex].strip().replace(",", ""))
                ),
                "account_id": 8,  # 직장인우대통장
            }

            models.Transaction(**parse_data).save()


if __name__ == "__main__":
    run()
