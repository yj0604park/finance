from django.urls import path

from money import helper, views
from money.view import transaction_view

app_name = "money"

urlpatterns = [
    path("", view=views.home_view, name="home"),
    path("bank_detail/<int:pk>", view=views.bank_detail_view, name="bank_detail"),
    path("bank_list", view=views.bank_list_view, name="bank_list"),
    path(
        "account_detail/<int:pk>", view=views.account_detail_view, name="account_detail"
    ),
    path(
        "category_detail/<str:category_type>",
        view=views.category_detail_view,
        name="category_detail",
    ),
    path("detail_item_list", view=views.detail_item_list_view, name="detail_item_list"),
    path(
        "detail_item_create",
        view=views.detail_item_create_view,
        name="detail_item_create",
    ),
    path(
        "retailer_summary",
        view=views.retailer_summary_view,
        name="retailer_summary",
    ),
    path(
        "retailer_detail/<int:pk>",
        view=views.retailer_detail_view,
        name="retailer_detail",
    ),
    path("retailer_create", view=views.retailer_create_view, name="retailer_create"),
    path("salary_list", view=views.salary_list_view, name="salary_list"),
    path("salary_detail/<int:pk>", view=views.salary_detail_view, name="salary_detail"),
    path("salary_create", view=views.salary_create_view, name="salary_create"),
    # Transaction
    path(
        "transaction_list",
        view=transaction_view.transaction_list_view,
        name="transaction_list",
    ),
    path(
        "transaction_create/<int:account_id>",
        view=transaction_view.transaction_create_view,
        name="transaction_create",
    ),
    path(
        "transaction_detail/<int:pk>",
        view=transaction_view.transaction_detail_view,
        name="transaction_detail",
    ),
    path(
        "transaction_category",
        view=transaction_view.transaction_category_view,
        name="transaction_category",
    ),
    path(
        "review_transaction",
        view=transaction_view.review_transaction_view,
        name="review_transaction",
    ),
    path(
        "review_internal",
        view=transaction_view.review_internal_transaction_view,
        name="review_internal_transaction",
    ),
    path(
        "review_detail_transaction",
        view=transaction_view.review_detail_transaction_view,
        name="review_detail_transaction",
    ),
    path(
        "transaction_detail_create/<int:transaction_id>",
        view=transaction_view.transaction_detail_create_view,
        name="transaction_detail_create",
    ),
    path("stock_create", view=views.stock_create_view, name="stock_create"),
    path("stock_detail/<int:pk>", view=views.stock_detail_view, name="stock_detail"),
    path(
        "stock_transaction_create/<int:account_id>",
        view=transaction_view.stock_transaction_create_view,
        name="stock_transaction_create",
    ),
    path(
        "stock_transaction_detail/<int:pk>",
        view=transaction_view.stock_transaction_detail_view,
        name="stock_transaction_detail",
    ),
    path("amazon_list", view=transaction_view.amazon_list_view, name="amazon_list"),
    path(
        "amazon_order_list",
        view=transaction_view.amazon_order_list_view,
        name="amazon_order_list",
    ),
    path(
        "update_balance/<int:account_id>",
        view=helper.update_balance,
        name="update_balance",
    ),
    path(
        "set_detail_required",
        view=helper.set_detail_required,
        name="set_detail_required",
    ),
    path(
        "update_related_trasaction",
        view=helper.update_related_transaction,
        name="update_related_transaction",
    ),
    path(
        "update_retailer_type",
        view=helper.update_retailer_type,
        name="update_retailer_type",
    ),
    path(
        "get_retailer_type/<int:retailer_id>",
        view=helper.get_retailer_type,
        name="get_retailer_type",
    ),
    path(
        "transaction/toggle_reviewed/<int:transaction_id>",
        view=helper.toggle_reviewed,
        name="toggle_reviewed",
    ),
]
