from django.urls import path

from money import helper, views

app_name = "money"

urlpatterns = [
    path("", view=views.home_view, name="home"),
    path("bank/<int:pk>", view=views.bank_detail_view, name="bank"),
    path("bank_list", view=views.bank_list_view, name="bank_list"),
    path("account/<int:pk>", view=views.account_detail_view, name="account"),
    path(
        "update_balance/<int:account_id>",
        view=helper.update_balance,
        name="update_balance",
    ),
    path("transaction_list", view=views.transaction_list_view, name="transaction_list"),
    path(
        "add_transaction/<int:account_id>",
        view=views.add_transaction_view,
        name="add_transaction",
    ),
    path(
        "transaction_detail/<int:pk>",
        view=views.transaction_detail_view,
        name="transaction_detail",
    ),
    path(
        "transaction_category",
        view=views.transaction_category_view,
        name="transaction_category",
    ),
    path(
        "category_detail/<str:category_type>",
        view=views.category_detail_view,
        name="category_detail",
    ),
    path(
        "review_transaction",
        view=views.review_transaction_view,
        name="review_transaction",
    ),
    path(
        "review_internal",
        view=views.review_internal_transaction_view,
        name="review_internal_transaction",
    ),
    path(
        "review_detail_transaction",
        view=views.review_detail_transaction_view,
        name="review_detail_transaction",
    ),
    path(
        "set_detail_required",
        view=helper.set_detail_required,
        name="set_detail_required",
    ),
    path(
        "add_transaction_detail/<int:transaction_id>",
        view=views.transaction_detail_create_view,
        name="add_transaction_detail",
    ),
    path(
        "add_detail_item",
        view=views.detail_item_create_view,
        name="add_detail_item",
    ),
    path(
        "update_related_trasaction",
        view=helper.update_related_transaction,
        name="update_related_transaction",
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
]
