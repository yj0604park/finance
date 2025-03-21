from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from money import views
from money.schema import schema
from money.views import transaction_detail_view, transaction_view, view_functions

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
    path("exchange/exchange_list", view=views.exchange_list_view, name="exchange_list"),
    path(
        "amount_snapshot_list",
        view=views.amount_snapshot_list_view,
        name="amount_snapshot_list",
    ),
    path(
        "update_snapshot",
        view=view_functions.create_daily_snapshot,
        name="update_snapshot",
    ),
    # region Stock
    path(
        "get_stock_snapshot",
        view=view_functions.get_stock_snapshot,
        name="get_stock_snapshot",
    ),
    path(
        "stock_chart",
        view=views.stock_amount_chart_view,
        name="stock_chart",
    ),
    # endregion
    # Transaction
    path(
        "transaction_list",
        view=transaction_view.transaction_list_view,
        name="transaction_list",
    ),
    path(
        "transaction_chart_list",
        view=transaction_view.transaction_chart_list_view,
        name="transaction_chart_list",
    ),
    path(
        "transaction_create/<int:account_id>",
        view=transaction_view.transaction_create_view,
        name="transaction_create",
    ),
    path(
        "transaction_update/<int:pk>",
        view=transaction_view.transaction_update_view,
        name="transaction_update",
    ),
    path(
        "transaction_category",
        view=transaction_view.transaction_category_view,
        name="transaction_category",
    ),
    path(
        "yearly_summary",
        view=transaction_view.yearly_summary_view,
        name="yearly_summary",
    ),
    path(
        "tax",
        view=transaction_view.tax_view,
        name="tax",
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
        "amazon_order_create",
        view=transaction_view.amazon_order_create_view,
        name="amazon_order_create",
    ),
    path(
        "amazon_order_detail/<int:pk>",
        view=transaction_view.amazon_order_detail_view,
        name="amazon_order_detail",
    ),
    # transaction detail view
    path(
        "transaction_detail/<int:pk>",
        view=transaction_detail_view.transaction_detail_view,
        name="transaction_detail",
    ),
    path(
        "transaction_detail_create/<int:transaction_id>",
        view=transaction_detail_view.transaction_detail_create_view,
        name="transaction_detail_create",
    ),
    path(
        "detail_item_list",
        view=transaction_detail_view.detail_item_list_view,
        name="detail_item_list",
    ),
    path(
        "detail_item_create",
        view=transaction_detail_view.detail_item_create_view,
        name="detail_item_create",
    ),
    path(
        "detail_item_category/<str:category>",
        view=transaction_detail_view.detail_item_category_view,
        name="detail_item_category",
    ),
    # region functional views
    path(
        "update_balance/<int:account_id>",
        view=view_functions.update_balance,
        name="update_balance",
    ),
    path(
        "set_detail_required",
        view=view_functions.set_detail_required,
        name="set_detail_required",
    ),
    path(
        "update_related_trasaction",
        view=view_functions.update_related_transaction,
        name="update_related_transaction",
    ),
    path(
        "update_retailer_type",
        view=view_functions.update_retailer_type,
        name="update_retailer_type",
    ),
    path(
        "get_retailer_type/<int:retailer_id>",
        view=view_functions.get_retailer_type,
        name="get_retailer_type",
    ),
    path(
        "transaction/toggle_reviewed/<int:transaction_id>",
        view=view_functions.toggle_reviewed,
        name="toggle_reviewed",
    ),
    path(
        "get_exchange_rate",
        view=view_functions.get_exchange_rate,
        name="get_exchange_rate",
    ),
    path(
        "get_items_for_category",
        view=view_functions.get_items_for_category,
        name="get_items_for_category",
    ),
    path(
        "update_related_transaction_for_amazon",
        view=view_functions.update_related_transaction_for_amazon,
        name="update_related_transaction_for_amazon",
    ),
    path(
        "filter_retailer", view=view_functions.filter_retailer, name="filter_retailer"
    ),
    path("file_upload", view=view_functions.file_upload, name="file_upload"),
    path(
        "get_end_month_balance",
        view=view_functions.get_end_month_balance,
        name="get_end_month_balance",
    ),
    path("graphql", csrf_exempt(GraphQLView.as_view(schema=schema))),
    # endregion
]
