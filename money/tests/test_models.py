"""
Comprehensive unit tests for money app models.

Covers: Bank, Account, AmountSnapshot, Transaction, TransactionDetail,
        Retailer, DetailItem, AmazonOrder, Stock, StockTransaction.
"""

import datetime
from decimal import Decimal

import pytest

from money.choices import (
    AccountType,
    CurrencyType,
    DetailItemCategory,
    RetailerType,
    TransactionCategory,
)
from money.models.accounts import Account, AmountSnapshot, Bank
from money.models.shoppings import AmazonOrder, DetailItem, Retailer
from money.models.stocks import Stock, StockTransaction
from money.models.transactions import Transaction, TransactionDetail


# ---------------------------------------------------------------------------
# Bank
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestBankModel:
    def test_create_bank(self, bank):
        assert bank.pk is not None
        assert bank.name == "Test Bank"

    def test_bank_str(self, bank):
        assert str(bank) == "Test Bank"

    def test_bank_ordering(self, db):
        Bank.objects.create(name="Zebra Bank")
        Bank.objects.create(name="Alpha Bank")
        names = list(Bank.objects.values_list("name", flat=True))
        assert names == sorted(names)

    def test_bank_balance_empty(self, bank):
        """A bank with no accounts has an empty balance list."""
        assert bank.balance == []

    def test_bank_balance_single_currency(self, bank, account):
        """Bank balance sums account amounts for same currency."""
        Account.objects.create(
            name="Second Account",
            bank=bank,
            amount=Decimal("3000.00"),
            currency=CurrencyType.KRW,
            type=AccountType.SAVINGS_ACCOUNT,
        )
        balances = bank.balance
        krw_balance = next(b for b in balances if b.currency == CurrencyType.KRW)
        # account fixture has 10000, second account has 3000
        assert krw_balance.value == Decimal("13000.00")

    def test_bank_balance_multi_currency(self, bank, account, usd_account):
        """Bank balance returns separate entries per currency."""
        balances = bank.balance
        currencies = {b.currency for b in balances}
        assert CurrencyType.KRW in currencies
        assert CurrencyType.USD in currencies

    def test_bank_balance_multi_currency_values(self, bank, account, usd_account):
        krw = next(b for b in bank.balance if b.currency == CurrencyType.KRW)
        usd = next(b for b in bank.balance if b.currency == CurrencyType.USD)
        assert krw.value == Decimal("10000.00")
        assert usd.value == Decimal("1000.00")


# ---------------------------------------------------------------------------
# Account
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestAccountModel:
    def test_create_account(self, account):
        assert account.pk is not None
        assert account.name == "Test Checking"
        assert account.amount == Decimal("10000.00")

    def test_account_str(self, account):
        assert str(account) == "Test Checking"

    def test_account_type_method(self, account):
        assert account.account_type() == AccountType.CHECKING_ACCOUNT

    def test_account_default_active(self, account):
        assert account.is_active is True

    def test_account_default_currency(self, bank):
        """Default currency is USD when not specified."""
        acc = Account.objects.create(name="Default Currency", bank=bank, amount=0)
        assert acc.currency == CurrencyType.USD

    def test_account_inactive(self, bank):
        acc = Account.objects.create(
            name="Closed Account",
            bank=bank,
            amount=Decimal("0"),
            is_active=False,
        )
        assert acc.is_active is False

    def test_account_types(self, bank):
        """All account types can be persisted."""
        for account_type in AccountType:
            acc = Account.objects.create(
                name=f"Account {account_type}",
                bank=bank,
                amount=Decimal("0"),
                type=account_type,
            )
            assert acc.type == account_type

    def test_account_alias(self, bank):
        acc = Account.objects.create(
            name="Main Account",
            bank=bank,
            amount=Decimal("0"),
            alias="My Main",
        )
        assert acc.alias == "My Main"

    def test_account_first_added_default(self, account):
        assert account.first_added is False


# ---------------------------------------------------------------------------
# AmountSnapshot
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestAmountSnapshotModel:
    def test_create_snapshot(self, amount_snapshot):
        assert amount_snapshot.pk is not None
        assert amount_snapshot.date == datetime.date(2024, 1, 31)
        assert amount_snapshot.amount == Decimal("15000.00")

    def test_snapshot_str(self, amount_snapshot):
        assert str(amount_snapshot) == "2024-01-31: KRW"

    def test_snapshot_with_json_summary(self, db):
        snap = AmountSnapshot.objects.create(
            date=datetime.date(2024, 2, 1),
            amount=Decimal("20000.00"),
            currency=CurrencyType.KRW,
            summary={"bank1": 10000, "bank2": 10000},
        )
        assert snap.summary["bank1"] == 10000


# ---------------------------------------------------------------------------
# Retailer
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestRetailerModel:
    def test_create_retailer(self, retailer):
        assert retailer.pk is not None
        assert retailer.name == "Test Store"

    def test_retailer_str(self, retailer):
        assert str(retailer) == "ETC: Test Store"

    def test_retailer_with_type(self, db):
        r = Retailer.objects.create(name="MyBank", type=RetailerType.BANK)
        assert str(r) == "BANK: MyBank"

    def test_retailer_default_category(self, retailer):
        assert retailer.category == TransactionCategory.ETC

    def test_retailer_ordering(self, db):
        Retailer.objects.create(name="Zara")
        Retailer.objects.create(name="Aldi")
        names = list(Retailer.objects.values_list("name", flat=True))
        assert names == sorted(names)


# ---------------------------------------------------------------------------
# DetailItem
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestDetailItemModel:
    def test_create_detail_item(self, detail_item):
        assert detail_item.pk is not None
        assert detail_item.name == "Apple"

    def test_detail_item_str(self, detail_item):
        # Default category is ETC
        assert str(detail_item) == "ETC-Apple"

    def test_detail_item_with_category(self, db):
        item = DetailItem.objects.create(name="Banana", category=DetailItemCategory.FRUIT)
        assert str(item) == "FRUIT-Banana"

    def test_detail_item_ordering(self, db):
        DetailItem.objects.create(name="Zucchini")
        DetailItem.objects.create(name="Apple")
        names = list(DetailItem.objects.values_list("name", flat=True))
        assert names == sorted(names)


# ---------------------------------------------------------------------------
# Transaction
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestTransactionModel:
    def test_create_transaction(self, transaction):
        assert transaction.pk is not None
        assert transaction.amount == Decimal("-500.00")
        assert transaction.account.name == "Test Checking"

    def test_transaction_str(self, transaction):
        result = str(transaction)
        assert "2024-01-15" in result
        assert "Test Checking" in result
        assert "Test Store" in result

    def test_transaction_str_no_retailer(self, db, account):
        txn = Transaction.objects.create(
            account=account,
            date=datetime.date(2024, 1, 20),
            amount=Decimal("1000.00"),
            type=TransactionCategory.INCOME,
        )
        result = str(txn)
        assert "None" in result  # retailer is None

    def test_transaction_default_not_internal(self, transaction):
        assert transaction.is_internal is False

    def test_transaction_default_not_reviewed(self, transaction):
        assert transaction.reviewed is False

    def test_transaction_default_category(self, db, account):
        txn = Transaction.objects.create(
            account=account,
            date=datetime.date(2024, 1, 1),
            amount=Decimal("0"),
        )
        assert txn.type == TransactionCategory.ETC

    def test_transaction_with_note(self, transaction):
        assert transaction.note == "Weekly groceries"

    def test_transaction_related_transaction(self, db, account, second_account):
        """Internal transfer: two transactions linked by related_transaction."""
        out_txn = Transaction.objects.create(
            account=account,
            date=datetime.date(2024, 2, 1),
            amount=Decimal("-2000.00"),
            is_internal=True,
            type=TransactionCategory.TRANSFER,
        )
        in_txn = Transaction.objects.create(
            account=second_account,
            date=datetime.date(2024, 2, 1),
            amount=Decimal("2000.00"),
            is_internal=True,
            related_transaction=out_txn,
            type=TransactionCategory.TRANSFER,
        )
        out_txn.related_transaction = in_txn
        out_txn.save()

        out_txn.refresh_from_db()
        assert out_txn.related_transaction == in_txn
        assert in_txn.related_transaction == out_txn

    def test_transaction_get_absolute_url(self, transaction):
        url = transaction.get_absolute_url()
        assert f"/money/transaction_detail/{transaction.pk}" in url

    def test_transaction_categories(self, db, account):
        """All transaction categories can be saved."""
        for category in TransactionCategory:
            txn = Transaction.objects.create(
                account=account,
                date=datetime.date(2024, 1, 1),
                amount=Decimal("0"),
                type=category,
            )
            assert txn.type == category


# ---------------------------------------------------------------------------
# TransactionDetail
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestTransactionDetailModel:
    def test_create_transaction_detail(self, db, transaction, detail_item):
        td = TransactionDetail.objects.create(
            transaction=transaction,
            item=detail_item,
            count=Decimal("3"),
            amount=Decimal("150.00"),
        )
        assert td.pk is not None
        assert td.count == Decimal("3")
        assert td.amount == Decimal("150.00")

    def test_transaction_detail_default_count(self, db, transaction, detail_item):
        td = TransactionDetail.objects.create(
            transaction=transaction,
            item=detail_item,
            amount=Decimal("100.00"),
        )
        assert td.count == Decimal("1")

    def test_transaction_detail_with_note(self, db, transaction, detail_item):
        td = TransactionDetail.objects.create(
            transaction=transaction,
            item=detail_item,
            amount=Decimal("50.00"),
            note="Organic",
        )
        assert td.note == "Organic"


# ---------------------------------------------------------------------------
# AmazonOrder
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestAmazonOrderModel:
    def test_create_amazon_order(self, amazon_order):
        assert amazon_order.pk is not None
        assert amazon_order.item == "Wireless Keyboard"
        assert amazon_order.is_returned is False

    def test_amazon_order_str(self, amazon_order):
        assert str(amazon_order) == "2024-01-10 Wireless Keyboard"

    def test_amazon_order_returned(self, db):
        order = AmazonOrder.objects.create(
            date=datetime.date(2024, 3, 1),
            item="Defective Item",
            is_returned=True,
        )
        assert order.is_returned is True

    def test_amazon_order_with_transaction(self, db, transaction):
        order = AmazonOrder.objects.create(
            date=datetime.date(2024, 1, 10),
            item="Book",
            transaction=transaction,
        )
        assert order.transaction == transaction

    def test_amazon_order_ordering(self, db):
        AmazonOrder.objects.create(date=datetime.date(2024, 3, 1), item="C")
        AmazonOrder.objects.create(date=datetime.date(2024, 1, 1), item="A")
        AmazonOrder.objects.create(date=datetime.date(2024, 2, 1), item="B")
        dates = list(AmazonOrder.objects.values_list("date", flat=True))
        assert dates == sorted(dates)

    def test_amazon_order_get_absolute_url(self, amazon_order):
        url = amazon_order.get_absolute_url()
        assert str(amazon_order.pk) in url


# ---------------------------------------------------------------------------
# Stock & StockTransaction
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestStockModel:
    def test_create_stock(self, db):
        stock = Stock.objects.create(name="Apple Inc", ticker="AAPL")
        assert stock.pk is not None
        assert stock.ticker == "AAPL"

    def test_stock_str(self, db):
        stock = Stock.objects.create(name="Microsoft", ticker="MSFT")
        assert str(stock) == "MSFT: Microsoft"

    def test_stock_str_no_ticker(self, db):
        stock = Stock.objects.create(name="Private Co", ticker=None)
        assert "None" in str(stock)

    def test_stock_ordering(self, db):
        Stock.objects.create(name="Zeta Corp", ticker="ZEP")
        Stock.objects.create(name="Alpha Inc", ticker="AAA")
        tickers = list(Stock.objects.values_list("ticker", flat=True))
        assert tickers == sorted(tickers)


@pytest.mark.django_db
class TestStockTransactionModel:
    @pytest.fixture
    def stock(self, db):
        return Stock.objects.create(name="Apple Inc", ticker="AAPL")

    def test_create_stock_transaction(self, db, account, stock):
        st = StockTransaction.objects.create(
            account=account,
            stock=stock,
            date=datetime.date(2024, 1, 15),
            amount=Decimal("1500.00"),
            price=Decimal("150.00"),
            shares=Decimal("10.0000"),
        )
        assert st.pk is not None
        assert st.shares == Decimal("10.0000")
        assert st.price == Decimal("150.00")

    def test_stock_transaction_str(self, db, account, stock):
        st = StockTransaction.objects.create(
            account=account,
            stock=stock,
            date=datetime.date(2024, 2, 20),
            amount=Decimal("3000.00"),
            price=Decimal("200.00"),
            shares=Decimal("15.0000"),
        )
        result = str(st)
        assert "2024-02-20" in result
        assert "AAPL" in result
        assert "15.0000" in result

    def test_stock_transaction_default_balance(self, db, account, stock):
        st = StockTransaction.objects.create(
            account=account,
            stock=stock,
            date=datetime.date(2024, 1, 1),
            amount=Decimal("0"),
            price=Decimal("100.00"),
            shares=Decimal("5.0000"),
        )
        assert st.balance == Decimal("0")
