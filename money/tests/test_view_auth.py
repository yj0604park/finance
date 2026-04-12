"""
모든 money 앱 뷰가 LoginRequiredMixin으로 보호되는지 검증.
미인증 요청은 로그인 페이지로 리다이렉트되어야 한다.
"""

import datetime
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from money.choices import AccountType, CurrencyType, TransactionCategory
from money.models.accounts import Bank, Account
from money.models.shoppings import Retailer
from money.models.transactions import Transaction

User = get_user_model()


def _redirect_to_login(response) -> bool:
    """응답이 로그인 페이지 리다이렉트인지 확인."""
    return response.status_code == 302 and (
        "/accounts/login/" in response["Location"]
        or "/accounts/" in response["Location"]
    )


class ViewAuthenticationTests(TestCase):
    """인증 없이 접근 시 로그인 페이지로 리다이렉트되는지 검증."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="pass")
        cls.bank = Bank.objects.create(name="Test Bank")
        cls.account = Account.objects.create(
            name="My Account",
            bank=cls.bank,
            amount=Decimal("1000.00"),
            currency=CurrencyType.KRW,
            type=AccountType.CHECKING_ACCOUNT,
        )
        cls.retailer = Retailer.objects.create(name="Store")
        cls.transaction = Transaction.objects.create(
            account=cls.account,
            date=datetime.date(2024, 1, 1),
            amount=Decimal("-100.00"),
            type=TransactionCategory.GROCERY,
        )

    def setUp(self):
        self.client = Client()  # 미인증 클라이언트

    # --- Bank views ---
    def test_bank_list_requires_login(self):
        res = self.client.get("/money/bank_list")
        self.assertTrue(
            _redirect_to_login(res), f"Expected redirect, got {res.status_code}"
        )

    def test_bank_detail_requires_login(self):
        res = self.client.get(f"/money/bank_detail/{self.bank.pk}")
        self.assertTrue(_redirect_to_login(res))

    # --- Account views ---
    def test_account_detail_requires_login(self):
        res = self.client.get(f"/money/account_detail/{self.account.pk}")
        self.assertTrue(_redirect_to_login(res))

    # --- Transaction views ---
    def test_transaction_list_requires_login(self):
        res = self.client.get("/money/")
        self.assertTrue(_redirect_to_login(res))

    # --- Exchange views ---
    def test_exchange_list_requires_login(self):
        res = self.client.get("/money/exchange/exchange_list")
        self.assertTrue(_redirect_to_login(res))

    # --- Salary views ---
    def test_salary_list_requires_login(self):
        res = self.client.get("/money/salary_list")
        self.assertTrue(_redirect_to_login(res))

    # --- GraphQL requires authentication ---
    def test_graphql_unauthenticated_redirects_or_requires_auth(self):
        """GraphQL 엔드포인트는 미인증 상태에서 로그인 페이지로 리다이렉트해야 한다."""
        res = self.client.post(
            "/money/graphql",
            data='{"query": "{ bankRelay { edges { node { id } } } }"}',
            content_type="application/json",
        )
        # 리다이렉트(302) 또는 인증 오류(401/403) 중 하나여야 함
        self.assertIn(res.status_code, [302, 401, 403])


class ViewAccessAuthenticatedTests(TestCase):
    """인증된 사용자는 뷰에 접근할 수 있는지 검증."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="authuser", password="pass")
        cls.bank = Bank.objects.create(name="Auth Bank")
        cls.account = Account.objects.create(
            name="Auth Account",
            bank=cls.bank,
            amount=Decimal("5000.00"),
            currency=CurrencyType.KRW,
            type=AccountType.CHECKING_ACCOUNT,
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_bank_list_accessible_when_authenticated(self):
        res = self.client.get("/money/bank_list")
        self.assertEqual(res.status_code, 200)

    @pytest.mark.skipif(
        pytest.importorskip("django.db").connection.vendor == "sqlite"
        if False  # 실제 체크는 런타임에서 진행
        else False,
        reason="DISTINCT ON은 PostgreSQL 전용",
    )
    def test_bank_detail_accessible_when_authenticated(self):
        from django.db import connection

        if connection.vendor == "sqlite":
            pytest.skip("BankDetailView uses DISTINCT ON (PostgreSQL only)")
        res = self.client.get(f"/money/bank_detail/{self.bank.pk}")
        self.assertEqual(res.status_code, 200)

    def test_account_detail_accessible_when_authenticated(self):
        res = self.client.get(f"/money/account_detail/{self.account.pk}")
        self.assertEqual(res.status_code, 200)

    def test_salary_list_accessible_when_authenticated(self):
        res = self.client.get("/money/salary_list")
        self.assertEqual(res.status_code, 200)

    def test_exchange_list_accessible_when_authenticated(self):
        res = self.client.get("/money/exchange/exchange_list")
        self.assertEqual(res.status_code, 200)
