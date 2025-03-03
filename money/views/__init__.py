from money.views.accounts import account_detail_view, category_detail_view
from money.views.banks import bank_detail_view, bank_list_view
from money.views.dashboard import home_view
from money.views.exchanges import exchange_list_view
from money.views.retailers import (
    retailer_create_view,
    retailer_detail_view,
    retailer_summary_view,
)
from money.views.salaries import (
    salary_create_view,
    salary_detail_view,
    salary_list_view,
)
from money.views.snapshots import amount_snapshot_list_view
from money.views.stocks import stock_create_view, stock_detail_view

__all__ = [
    "home_view",
    "bank_detail_view",
    "bank_list_view",
    "account_detail_view",
    "category_detail_view",
    "retailer_create_view",
    "retailer_detail_view",
    "retailer_summary_view",
    "salary_create_view",
    "salary_detail_view",
    "salary_list_view",
    "stock_create_view",
    "stock_detail_view",
    "exchange_list_view",
    "amount_snapshot_list_view",
]
