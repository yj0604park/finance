"""
Tests for StockTransaction GraphQL filter using the nested StockFilter type.

Verifies that `stockTransactionRelay` with `{ stock: { id: { exact: stockId } } }`
correctly filters results after the fix to StockTransactionFilter.stock from
`auto` (IDBaseFilterLookup) to `StockFilter` (nested filter).
"""

import datetime
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from money.choices import AccountType, CurrencyType
from money.models.accounts import Account, Bank
from money.models.stocks import Stock, StockTransaction


@pytest.fixture
def bank(db):
    return Bank.objects.create(name="Stock Test Bank")


@pytest.fixture
def account(db, bank):
    return Account.objects.create(
        name="Stock Test Account",
        bank=bank,
        amount=Decimal("50000.00"),
        currency=CurrencyType.USD,
        type=AccountType.CHECKING_ACCOUNT,
    )


@pytest.fixture
def stock_a(db):
    return Stock.objects.create(name="Apple", ticker="AAPL", currency=CurrencyType.USD)


@pytest.fixture
def stock_b(db):
    return Stock.objects.create(name="Tesla", ticker="TSLA", currency=CurrencyType.USD)


@pytest.fixture
def stock_txn_a(db, account, stock_a):
    return StockTransaction.objects.create(
        account=account,
        stock=stock_a,
        date=datetime.date(2024, 6, 1),
        price=Decimal("180.00"),
        amount=Decimal("1800.00"),
        shares=Decimal("10.0000"),
    )


@pytest.fixture
def stock_txn_b(db, account, stock_b):
    return StockTransaction.objects.create(
        account=account,
        stock=stock_b,
        date=datetime.date(2024, 6, 2),
        price=Decimal("250.00"),
        amount=Decimal("2500.00"),
        shares=Decimal("10.0000"),
    )


class TestStockTransactionRelayFilter:
    """Tests for the stockTransactionRelay query with nested StockFilter."""

    def setup_method(self):
        User = get_user_model()
        self.user, _ = User.objects.get_or_create(
            username="stocktestuser",
            defaults={"email": "stocktest@example.com"},
        )
        self.user.set_password("testpassword")
        self.user.save()
        self.client = Client()
        self.client.login(username="stocktestuser", password="testpassword")

    @pytest.mark.django_db
    def test_filter_by_stock_id_returns_only_matching_transactions(self, stock_txn_a, stock_txn_b, stock_a):
        """stockTransactionRelay with { stock: { id: { exact: <id> } } } returns
        only transactions for that stock."""
        query = f"""
        query {{
          stockTransactionRelay(
            filters: {{ stock: {{ id: {{ exact: "{stock_a.id}" }} }} }}
          ) {{
            edges {{
              node {{
                id
              }}
            }}
            totalCount
          }}
        }}
        """

        response = self.client.post(
            "/money/graphql",
            {"query": query},
            content_type="application/json",
        )
        self.assert_no_errors(response)
        data = response.json()["data"]["stockTransactionRelay"]
        assert data["totalCount"] == 1, f"Expected 1 transaction for stock_a, got {data['totalCount']}"

    @pytest.mark.django_db
    def test_filter_with_exact_stock_id_excludes_other_stocks(self, stock_txn_a, stock_txn_b, stock_b):
        """Filtering by stock_b's id does not return stock_a's transactions."""
        query = f"""
        query {{
          stockTransactionRelay(
            filters: {{ stock: {{ id: {{ exact: "{stock_b.id}" }} }} }}
          ) {{
            edges {{
              node {{
                id
              }}
            }}
            totalCount
          }}
        }}
        """

        response = self.client.post(
            "/money/graphql",
            {"query": query},
            content_type="application/json",
        )
        self.assert_no_errors(response)
        data = response.json()["data"]["stockTransactionRelay"]
        assert data["totalCount"] == 1

    @pytest.mark.django_db
    def test_no_filter_returns_all_transactions(self, stock_txn_a, stock_txn_b):
        """Without filters, all transactions are returned."""
        query = """
        query {
          stockTransactionRelay {
            totalCount
          }
        }
        """
        response = self.client.post(
            "/money/graphql",
            {"query": query},
            content_type="application/json",
        )
        self.assert_no_errors(response)
        data = response.json()["data"]["stockTransactionRelay"]
        assert data["totalCount"] == 2

    def assert_no_errors(self, response):
        assert response.status_code == 200, f"HTTP {response.status_code}"
        content = response.json()
        assert "errors" not in content, f"GraphQL errors: {content.get('errors')}"
