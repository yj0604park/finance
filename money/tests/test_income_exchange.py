"""
Salary, W2, Exchange 모델 단위 테스트.
기존 test_models.py에서 누락된 재무 계산 관련 모델 보강.
"""

import datetime
from decimal import Decimal

import pytest

from money.choices import CurrencyType, ExchangeType
from money.models.exchanges import Exchange
from money.models.incomes import Salary, W2


# ---------------------------------------------------------------------------
# Salary 모델
# ---------------------------------------------------------------------------
@pytest.mark.django_db
class TestSalaryModel:
    def _make_salary(self, transaction, **kwargs):
        defaults = dict(
            date=datetime.date(2024, 1, 31),
            gross_pay=Decimal("5000.00"),
            total_adjustment=Decimal("100.00"),
            total_withheld=Decimal("800.00"),
            total_deduction=Decimal("200.00"),
            net_pay=Decimal("4000.00"),
            pay_detail={"base": "5000"},
            adjustment_detail={},
            tax_detail={"federal": "600", "state": "200"},
            deduction_detail={"health": "200"},
            currency=CurrencyType.USD,
            transaction=transaction,
        )
        defaults.update(kwargs)
        return Salary.objects.create(**defaults)

    def test_str_returns_date(self, transaction):
        salary = self._make_salary(transaction)
        assert str(salary) == "2024-01-31"

    def test_default_currency_is_usd(self, transaction):
        salary = self._make_salary(transaction)
        assert salary.currency == CurrencyType.USD

    def test_decimal_precision(self, transaction):
        salary = self._make_salary(
            transaction,
            gross_pay=Decimal("12345.67"),
            net_pay=Decimal("9876.54"),
        )
        s = Salary.objects.get(pk=salary.pk)
        assert s.gross_pay == Decimal("12345.67")
        assert s.net_pay == Decimal("9876.54")

    def test_json_fields_stored_and_retrieved(self, transaction):
        detail = {"base_pay": 5000, "bonus": 500, "overtime": 200}
        salary = self._make_salary(transaction, pay_detail=detail)
        s = Salary.objects.get(pk=salary.pk)
        assert s.pay_detail["base_pay"] == 5000
        assert s.pay_detail["bonus"] == 500

    def test_transaction_relationship(self, transaction):
        salary = self._make_salary(transaction)
        assert salary.transaction == transaction
        assert transaction.salary_set.filter(pk=salary.pk).exists()

    def test_krw_currency(self, transaction):
        salary = self._make_salary(transaction, currency=CurrencyType.KRW)
        assert salary.currency == CurrencyType.KRW

    def test_get_absolute_url(self, transaction):
        salary = self._make_salary(transaction)
        url = salary.get_absolute_url()
        assert f"{salary.pk}" in url


# ---------------------------------------------------------------------------
# W2 모델
# ---------------------------------------------------------------------------
@pytest.mark.django_db
class TestW2Model:
    def _make_w2(self, **kwargs):
        defaults = dict(
            date=datetime.date(2023, 1, 31),
            year=2022,
            wages=Decimal("60000.00"),
            income_tax=Decimal("8000.00"),
            social_security_wages=Decimal("60000.00"),
            social_security_tax=Decimal("3720.00"),
            medicare_wages=Decimal("60000.00"),
            medicare_tax=Decimal("870.00"),
            currency=CurrencyType.USD,
        )
        defaults.update(kwargs)
        return W2.objects.create(**defaults)

    def test_str_returns_date(self):
        w2 = self._make_w2()
        assert str(w2) == "2023-01-31"

    def test_year_field(self):
        w2 = self._make_w2(year=2023)
        assert w2.year == 2023

    def test_decimal_fields_stored_correctly(self):
        w2 = self._make_w2(
            wages=Decimal("75000.50"),
            income_tax=Decimal("12345.67"),
        )
        w2 = W2.objects.get(pk=w2.pk)
        assert w2.wages == Decimal("75000.50")
        assert w2.income_tax == Decimal("12345.67")

    def test_box_12_json_field(self):
        box12 = [{"code": "D", "amount": "1500.00"}, {"code": "W", "amount": "250.00"}]
        w2 = self._make_w2(box_12=box12)
        w2 = W2.objects.get(pk=w2.pk)
        assert len(w2.box_12) == 2
        assert w2.box_12[0]["code"] == "D"

    def test_box_14_optional(self):
        """box_14 는 null 허용."""
        w2 = self._make_w2(box_14=None)
        assert w2.box_14 is None

    def test_box_14_max_length(self):
        """box_14 는 최대 200자."""
        w2 = self._make_w2(box_14="A" * 200)
        w2 = W2.objects.get(pk=w2.pk)
        assert len(w2.box_14) == 200

    def test_multiple_years_queryable(self):
        self._make_w2(date=datetime.date(2022, 1, 31), year=2021)
        self._make_w2(date=datetime.date(2023, 1, 31), year=2022)
        self._make_w2(date=datetime.date(2024, 1, 31), year=2023)
        assert W2.objects.filter(year=2022).count() == 1
        assert W2.objects.count() == 3


# ---------------------------------------------------------------------------
# Exchange 모델
# ---------------------------------------------------------------------------
@pytest.mark.django_db
class TestExchangeModel:
    def _make_exchange(self, transaction, second_transaction=None, **kwargs):
        if second_transaction is None:
            second_transaction = transaction
        defaults = dict(
            date=datetime.date(2024, 2, 1),
            from_transaction=transaction,
            to_transaction=second_transaction,
            from_amount=Decimal("100.00"),
            to_amount=Decimal("130000.00"),
            from_currency=CurrencyType.USD,
            to_currency=CurrencyType.KRW,
            ratio_per_krw=Decimal("0.0008"),
            exchange_type=ExchangeType.ETC,
        )
        defaults.update(kwargs)
        return Exchange.objects.create(**defaults)

    def test_str_returns_date_and_ratio(self, transaction):
        ex = self._make_exchange(transaction, ratio_per_krw=Decimal("0.0008"))
        assert "2024-02-01" in str(ex)
        assert "0.0008" in str(ex)

    def test_from_to_currency_stored(self, transaction):
        ex = self._make_exchange(transaction)
        ex = Exchange.objects.get(pk=ex.pk)
        assert ex.from_currency == CurrencyType.USD
        assert ex.to_currency == CurrencyType.KRW

    def test_ratio_per_krw_precision(self, transaction):
        ex = self._make_exchange(transaction, ratio_per_krw=Decimal("0.0007654"))
        ex = Exchange.objects.get(pk=ex.pk)
        # 소수점 4자리까지 저장 (DB 반올림)
        assert ex.ratio_per_krw == Decimal("0.0008")

    def test_ratio_per_krw_nullable(self, transaction):
        ex = self._make_exchange(transaction, ratio_per_krw=None)
        assert ex.ratio_per_krw is None

    def test_exchange_type_default_etc(self, transaction):
        ex = Exchange.objects.create(
            date=datetime.date(2024, 2, 1),
            from_transaction=transaction,
            to_transaction=transaction,
            from_amount=Decimal("100.00"),
            to_amount=Decimal("130000.00"),
            from_currency=CurrencyType.USD,
            to_currency=CurrencyType.KRW,
        )
        assert ex.exchange_type == ExchangeType.ETC

    def test_transaction_reverse_relations(self, transaction):
        ex = self._make_exchange(transaction)
        assert transaction.exchange_from.filter(pk=ex.pk).exists()
        assert transaction.exchange_to.filter(pk=ex.pk).exists()

    def test_amounts_stored_correctly(self, transaction):
        ex = self._make_exchange(
            transaction,
            from_amount=Decimal("500.00"),
            to_amount=Decimal("650000.00"),
        )
        ex = Exchange.objects.get(pk=ex.pk)
        assert ex.from_amount == Decimal("500.00")
        assert ex.to_amount == Decimal("650000.00")
