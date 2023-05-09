import json
from money import models


def run():
    with open("", encoding="utf-8") as f:  # update file name
        # 직장인우대통장
        account = models.Account.objects.get(pk=8)

        for line in f:
            data = line.split("\t")

            parse_data = {
                "date": data[0].replace(".", "-")[:10],
                "note": json.dumps(
                    {
                        "type": data[1],
                        "retailer": data[2],
                        "note": data[3],
                        "balance": float(data[6].strip().replace(",", "")),
                    },
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=False,
                ),
                "amount": -float(data[4].strip().replace(",", ""))
                if float(data[4].strip().replace(",", ""))
                else float(data[5].strip().replace(",", "")),
                "account_id": 8,
            }

            models.Transaction(**parse_data).save()


if __name__ == "__main__":
    run()
