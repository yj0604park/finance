import strawberry
import strawberry.django
from django.db.models import Sum
from strawberry_django import mutations
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry_django.relay import ListConnectionWithTotalCount

from money.models.incomes import Salary
from money.types import types
from money.types.accounts import (
    AccountInput,
    AccountNode,
    AccountPartialInput,
    AmountSnapshotNode,
    BankNode,
)
from money.types.credit_cards import (
    CreditCardBenefitInput,
    CreditCardBenefitNode,
    CreditCardInput,
    CreditCardNode,
)
from money.types.exchanges import ExchangeNode
from money.types.incomes import SalaryInput, SalaryNode, SalaryPartialInput
from money.types.retailers import RetailerInput, RetailerNode
from money.types.shoppings import AmazonOrderInput, AmazonOrderNode
from money.types.stocks import (
    StockInput,
    StockNode,
    StockPriceInput,
    StockPriceNode,
    StockTransactionInput,
    StockTransactionNode,
    StockTransactionPartialInput,
)
from money.types.transactions import TransactionInput, TransactionNode


def get_salary_years() -> list[int]:
    return list(Salary.objects.values_list("date__year", flat=True).distinct().order_by("date__year"))


def get_salary_summary() -> list[types.SalarySummaryNode]:
    summary_rows = Salary.objects.values("date__year").annotate(total_gross_pay=Sum("gross_pay")).order_by("date__year")

    return [
        types.SalarySummaryNode(
            year=row["date__year"],
            total_gross_pay=row["total_gross_pay"],
        )
        for row in summary_rows
    ]


@strawberry.type
class Query:
    transaction_relay: ListConnectionWithTotalCount[TransactionNode] = strawberry.django.connection()

    retailer_relay: ListConnectionWithTotalCount[RetailerNode] = strawberry.django.connection()

    bank_relay: ListConnectionWithTotalCount[BankNode] = strawberry.django.connection()

    account_relay: ListConnectionWithTotalCount[AccountNode] = strawberry.django.connection()

    amountSnapshot_relay: ListConnectionWithTotalCount[AmountSnapshotNode] = strawberry.django.connection()

    salary_relay: ListConnectionWithTotalCount[SalaryNode] = strawberry.django.connection()

    stock_relay: ListConnectionWithTotalCount[StockNode] = strawberry.django.connection()

    stock_transaction_relay: ListConnectionWithTotalCount[StockTransactionNode] = strawberry.django.connection()

    stock_price_relay: ListConnectionWithTotalCount[StockPriceNode] = strawberry.django.connection()

    amazon_order_relay: ListConnectionWithTotalCount[AmazonOrderNode] = strawberry.django.connection()

    exchange_relay: ListConnectionWithTotalCount[ExchangeNode] = strawberry.django.connection()

    credit_card_relay: ListConnectionWithTotalCount[CreditCardNode] = strawberry.django.connection()

    salary_years: list[int] = strawberry.field(resolver=get_salary_years)
    salary_summary: list[types.SalarySummaryNode] = strawberry.field(resolver=get_salary_summary)


@strawberry.type
class Mutation:
    create_account: AccountNode = mutations.create(AccountInput)
    update_account: AccountNode = mutations.update(AccountPartialInput)
    create_transaction: TransactionNode = mutations.create(TransactionInput)
    create_retailer: RetailerNode = mutations.create(RetailerInput)
    create_stock: StockNode = mutations.create(StockInput)
    create_stock_transaction: StockTransactionNode = mutations.create(StockTransactionInput)
    update_stock_transaction: StockTransactionNode = mutations.update(StockTransactionPartialInput)
    create_stock_price: StockPriceNode = mutations.create(StockPriceInput)
    create_amazon_order: AmazonOrderNode = mutations.create(AmazonOrderInput)
    create_credit_card: CreditCardNode = mutations.create(CreditCardInput)
    create_credit_card_benefit: CreditCardBenefitNode = mutations.create(CreditCardBenefitInput)
    create_salary: SalaryNode = mutations.create(SalaryInput)
    update_salary: SalaryNode = mutations.update(SalaryPartialInput)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
