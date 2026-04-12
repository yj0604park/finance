"""
Shared pytest fixtures for the money app tests.
"""

import datetime
from decimal import Decimal

import pytest

from money.choices import AccountType, CurrencyType, TransactionCategory
from money.models.accounts import Account, AmountSnapshot, Bank
from money.models.shoppings import AmazonOrder, DetailItem, Retailer
from money.models.transactions import Transaction


@pytest.fixture
def bank(db):
    return Bank.objects.create(name="Test Bank")


@pytest.fixture
def account(db, bank):
    return Account.objects.create(
        name="Test Checking",
        bank=bank,
        amount=Decimal("10000.00"),
        currency=CurrencyType.KRW,
        type=AccountType.CHECKING_ACCOUNT,
    )


@pytest.fixture
def second_account(db, bank):
    return Account.objects.create(
        name="Test Savings",
        bank=bank,
        amount=Decimal("5000.00"),
        currency=CurrencyType.KRW,
        type=AccountType.SAVINGS_ACCOUNT,
    )


@pytest.fixture
def usd_account(db, bank):
    return Account.objects.create(
        name="USD Account",
        bank=bank,
        amount=Decimal("1000.00"),
        currency=CurrencyType.USD,
        type=AccountType.CHECKING_ACCOUNT,
    )


@pytest.fixture
def retailer(db):
    return Retailer.objects.create(name="Test Store")


@pytest.fixture
def transaction(db, account, retailer):
    return Transaction.objects.create(
        account=account,
        date=datetime.date(2024, 1, 15),
        amount=Decimal("-500.00"),
        retailer=retailer,
        type=TransactionCategory.GROCERY,
        note="Weekly groceries",
    )


@pytest.fixture
def detail_item(db):
    return DetailItem.objects.create(name="Apple")


@pytest.fixture
def amazon_order(db):
    return AmazonOrder.objects.create(
        date=datetime.date(2024, 1, 10),
        item="Wireless Keyboard",
    )


@pytest.fixture
def amount_snapshot(db):
    return AmountSnapshot.objects.create(
        date=datetime.date(2024, 1, 31),
        amount=Decimal("15000.00"),
        currency=CurrencyType.KRW,
    )
