from collections import defaultdict
from decimal import Decimal

from money.choices import CurrencyType
from money.helpers.helper import (
    bank_summary,
    filter_by_currency,
    get_saving_interest_tax_summary,
)
from money.models.incomes import Salary
from money.models.transactions import Transaction


def year_summary(target_year: int):
    """
    Get all transactions in the year and return summary.
    """
    this_year_transactions = (
        Transaction.objects.prefetch_related("account")
        .filter(date__year=target_year, account__bank__id=5)
        .order_by("date", "-amount")
    )

    account_summary = {}

    for transaction in this_year_transactions:
        account = transaction.account
        if account not in account_summary:
            account_summary[account] = {
                "max_value": 0.0,
                "max_date": None,
                "last_value": 0.0,
            }

        if transaction.balance is not None:
            current_max = account_summary[account]["max_value"]

            if current_max < transaction.balance:
                account_summary[account]["max_value"] = max(
                    current_max, transaction.balance
                )
                account_summary[account]["max_date"] = transaction.date

            account_summary[account]["last_value"] = transaction.balance
        else:
            print(f"{transaction} is not updated")

    account_summary = account_summary.items()

    # Salary summary
    salary = Salary.objects.filter(date__year=target_year)
    salary_info = {
        "total_grosspay": Decimal(0.0),
        "401(K)": 0.0,
        "federal_tax": 0.0,
        "patent_award": 0.0,
        "vacation_payout": 0.0,
        "social_security_tax": 0.0,
        "medicare_tax": 0.0,
        "stock_award": 0.0,
        "relocation": 0.0,
        "total_pay_detail": defaultdict(float),
        "total_adjustment_detail": defaultdict(float),
        "total_tax_detail": defaultdict(float),
        "total_deduction_detail": defaultdict(float),
    }

    for s in salary:
        salary_info["total_grosspay"] += s.gross_pay
        if "Patent Award" in s.pay_detail:
            salary_info["patent_award"] += s.pay_detail["Patent Award"]
        if "Vacation Payout" in s.pay_detail:
            salary_info["vacation_payout"] += s.pay_detail["Vacation Payout"]

        salary_info["401(K)"] += s.adjustment_detail["401(K)"]
        if "Stock Award Income" in s.adjustment_detail:
            salary_info["stock_award"] += s.adjustment_detail["Stock Award Income"]
        if "Relo expense - taxable" in s.adjustment_detail:
            salary_info["relocation"] += s.adjustment_detail["Relo expense - taxable"]
        if "Relo Expense Total Taxes" in s.adjustment_detail:
            salary_info["relocation"] += s.adjustment_detail["Relo Expense Total Taxes"]

        salary_info["federal_tax"] -= s.tax_detail["Federal income tax"]
        if "Social security tax" in s.tax_detail:
            salary_info["social_security_tax"] -= s.tax_detail["Social security tax"]
        if "Medicare tax" in s.tax_detail:
            salary_info["medicare_tax"] -= s.tax_detail["Medicare tax"]

        for k, v in s.pay_detail.items():
            salary_info["total_pay_detail"][k] += v
        for k, v in s.adjustment_detail.items():
            salary_info["total_adjustment_detail"][k] += v
        for k, v in s.tax_detail.items():
            salary_info["total_tax_detail"][k] += v
        for k, v in s.deduction_detail.items():
            salary_info["total_deduction_detail"][k] += v

    context = {
        "target_year": target_year,
        "this_year_transactions": this_year_transactions,
        "account_summary_krw": filter_by_currency(account_summary, CurrencyType.KRW),
        "account_summary_usd": filter_by_currency(account_summary, CurrencyType.USD),
        "saving_interest_tax": get_saving_interest_tax_summary(target_year),
        "salary": salary_info,
        "bank": bank_summary(target_year),
    }

    return context
