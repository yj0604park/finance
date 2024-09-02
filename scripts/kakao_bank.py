import json

from money import models


def run():
    with open("data/kakao_bank_2024_05.tsv", encoding="utf-8") as f:  # update file name
        # 카카오 입출금통장
        account = models.Account.objects.get(pk=9)

        for line in f:
            data = line.split("\t")

            parse_data = {
                "date": data[0].replace(".", "-")[:10],
                "note": json.dumps(
                    {
                        "type": data[1],
                        "retailer": data[5].strip(),
                        "note": data[4],
                        "balance": float(data[3].strip().replace(",", "")),
                    },
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=False,
                ),
                "amount": float(data[2].strip().replace(",", "")),
                "account_id": account.id,
            }

            models.Transaction(**parse_data).save()


if __name__ == "__main__":
    run()
