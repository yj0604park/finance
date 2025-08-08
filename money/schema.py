import strawberry
import strawberry.django
from django.db.models import Sum
from strawberry_django import mutations
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry_django.relay import ListConnectionWithTotalCount

from money.models.incomes import Salary
from money.types import types
from money.types.accounts import AccountInput, AccountNode, AmountSnapshotNode, BankNode
from money.types.incomes import SalaryNode
from money.types.retailers import RetailerInput, RetailerNode
from money.types.shoppings import AmazonOrderInput, AmazonOrderNode
from money.types.stocks import (
    StockInput,
    StockNode,
    StockTransactionInput,
    StockTransactionNode,
)
from money.types.transactions import TransactionInput, TransactionNode


def get_salary_years() -> list[int]:
    return list(
        Salary.objects.values_list("date__year", flat=True)
        .distinct()
        .order_by("date__year")
    )


def get_salary_summary() -> list[types.SalarySummaryNode]:
    summary_rows = (
        Salary.objects.values("date__year")
        .annotate(total_gross_pay=Sum("gross_pay"))
        .order_by("date__year")
    )

    return [
        types.SalarySummaryNode(
            year=row["date__year"],
            total_gross_pay=row["total_gross_pay"],
        )
        for row in summary_rows
    ]


@strawberry.type
class Query:
    transaction_relay: ListConnectionWithTotalCount[
        TransactionNode
    ] = strawberry.django.connection()

    retailer_relay: ListConnectionWithTotalCount[
        RetailerNode
    ] = strawberry.django.connection()

    bank_relay: ListConnectionWithTotalCount[BankNode] = strawberry.django.connection()

    account_relay: ListConnectionWithTotalCount[
        AccountNode
    ] = strawberry.django.connection()

    amountSnapshot_relay: ListConnectionWithTotalCount[
        AmountSnapshotNode
    ] = strawberry.django.connection()

    salary_relay: ListConnectionWithTotalCount[
        SalaryNode
    ] = strawberry.django.connection()

    stock_relay: ListConnectionWithTotalCount[
        StockNode
    ] = strawberry.django.connection()

    amazon_order_relay: ListConnectionWithTotalCount[
        AmazonOrderNode
    ] = strawberry.django.connection()

    salary_years: list[int] = strawberry.field(resolver=get_salary_years)
    salary_summary: list[types.SalarySummaryNode] = strawberry.field(
        resolver=get_salary_summary
    )


@strawberry.type
class Mutation:
    create_account: AccountNode = mutations.create(AccountInput)
    create_transaction: TransactionNode = mutations.create(TransactionInput)
    create_retailer: RetailerNode = mutations.create(RetailerInput)
    create_stock: StockNode = mutations.create(StockInput)
    create_stock_transaction: StockTransactionNode = mutations.create(
        StockTransactionInput
    )
    create_amazon_order: AmazonOrderNode = mutations.create(AmazonOrderInput)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
