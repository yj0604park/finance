from django.urls import path

from money import views

app_name = "money"

urlpatterns = [
    path("", view=views.home_view, name="home"),
    path("bank/<int:pk>", view=views.bank_detail_view, name="bank"),
    path("bank_list", view=views.bank_list_view, name="bank_list"),
    path("account/<int:pk>", view=views.account_detail_view, name="account"),
    path(
        "update_balance/<int:account_id>",
        view=views.updateBalance,
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
]
