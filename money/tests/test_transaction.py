from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from money.models import Account, Bank, Category, Retailer, Transaction


class TransactionCreateViewTest(TestCase):
    """거래 생성 뷰를 테스트하는 클래스"""

    def setUp(self):
        """테스트에 필요한 데이터를 설정합니다."""
        # 사용자 생성
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        # 은행 생성
        self.bank = Bank.objects.create(name="Test Bank")

        # 계좌 생성
        self.account = Account.objects.create(
            name="Test Account",
            bank=self.bank,
            amount=1000,
            currency="KRW",
            type="CHECKING",
        )

        # 판매자 생성
        self.retailer = Retailer.objects.create(name="Test Retailer")

        # 카테고리 생성
        self.category = Category.objects.create(name="Test Category")

        # 클라이언트 설정
        self.client = Client()

        # 로그인
        self.client.login(username="testuser", password="testpassword")

    def test_transaction_create_view_get(self):
        """GET 요청으로 거래 생성 페이지에 접근할 수 있는지 테스트합니다."""
        url = reverse(
            "money:transaction_create", kwargs={"account_id": self.account.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transaction/transaction_create.html")
        self.assertContains(response, self.account.name)

    def test_transaction_create_view_post(self):
        """POST 요청으로 거래를 생성할 수 있는지 테스트합니다."""
        url = reverse(
            "money:transaction_create", kwargs={"account_id": self.account.id}
        )

        # 거래 생성 데이터
        data = {
            "account": self.account.id,
            "date": timezone.now().date(),
            "amount": 500,
            "retailer": self.retailer.id,
            "category": self.category.id,
            "note": "테스트 거래",
        }

        # 거래 생성 요청
        response = self.client.post(url, data)

        # 리다이렉트 여부 확인 (성공 시 리다이렉트됨)
        self.assertEqual(response.status_code, 302)

        # 거래가 생성되었는지 확인
        self.assertTrue(Transaction.objects.filter(note="테스트 거래").exists())

        # 생성된 거래 정보 확인
        transaction = Transaction.objects.get(note="테스트 거래")
        self.assertEqual(transaction.amount, 500)
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.retailer, self.retailer)

    def test_transaction_create_internal(self):
        """내부 거래(계좌 간 이체)를 생성할 수 있는지 테스트합니다."""
        # 두 번째 계좌 생성
        second_account = Account.objects.create(
            name="Second Account",
            bank=self.bank,
            amount=2000,
            currency="KRW",
            type="SAVINGS",
        )

        url = reverse(
            "money:transaction_create", kwargs={"account_id": self.account.id}
        )

        # 내부 거래 데이터
        data = {
            "account": self.account.id,
            "date": timezone.now().date(),
            "amount": -300,  # 출금
            "note": "내부 거래 테스트",
            "is_internal": True,
            "related_account": second_account.id,
        }

        # 거래 생성 요청
        response = self.client.post(url, data)

        # 리다이렉트 여부 확인
        self.assertEqual(response.status_code, 302)

        # 거래가 생성되었는지 확인
        self.assertTrue(Transaction.objects.filter(note="내부 거래 테스트").exists())

        # 두 계좌의 잔액 변화 확인
        self.account.refresh_from_db()
        second_account.refresh_from_db()

        # 원래 계좌는 출금되었으므로 잔액이 감소
        self.assertEqual(self.account.amount, 700)
        # 두 번째 계좌는 입금되었으므로 잔액이 증가
        self.assertEqual(second_account.amount, 2300)


class TransactionAPITest(TestCase):
    """GraphQL API를 통한 거래 생성을 테스트하는 클래스"""

    def setUp(self):
        """테스트에 필요한 데이터를 설정합니다."""
        # 사용자 생성
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        # 은행 생성
        self.bank = Bank.objects.create(name="Test Bank")

        # 계좌 생성
        self.account = Account.objects.create(
            name="Test Account",
            bank=self.bank,
            amount=1000,
            currency="KRW",
            type="CHECKING",
        )

        # 클라이언트 설정
        self.client = Client()

        # 로그인
        self.client.login(username="testuser", password="testpassword")

    def test_create_transaction_mutation(self):
        """GraphQL createTransaction 뮤테이션을 테스트합니다."""
        query = (
            """
        mutation {
          createTransaction(
            amount: 500,
            date: "2023-01-01",
            accountId: "%s",
            note: "GraphQL 테스트 거래"
          ) {
            id
          }
        }
        """
            % self.account.id
        )

        # GraphQL 엔드포인트로 요청
        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )

        # 응답 확인
        self.assertEqual(response.status_code, 200)

        # JSON 응답에 에러가 없는지 확인
        content = response.json()
        self.assertNotIn("errors", content)

        # 거래가 생성되었는지 확인
        self.assertTrue(Transaction.objects.filter(note="GraphQL 테스트 거래").exists())

    def test_create_transaction_without_retailer(self):
        """판매자 없이 거래를 생성하는 뮤테이션을 테스트합니다."""
        query = (
            """
        mutation {
          createTransaction(
            amount: -200,
            date: "2023-01-02",
            accountId: "%s",
            isInternal: false,
            note: "판매자 없는 거래"
          ) {
            id
          }
        }
        """
            % self.account.id
        )

        # GraphQL 엔드포인트로 요청
        response = self.client.post(
            "/graphql/", {"query": query}, content_type="application/json"
        )

        # 응답 확인
        self.assertEqual(response.status_code, 200)

        # JSON 응답에 에러가 없는지 확인
        content = response.json()
        self.assertNotIn("errors", content)

        # 거래가 생성되었는지 확인
        self.assertTrue(Transaction.objects.filter(note="판매자 없는 거래").exists())

        # 생성된 거래 정보 확인
        transaction = Transaction.objects.get(note="판매자 없는 거래")
        self.assertEqual(transaction.amount, -200)
        self.assertEqual(transaction.account, self.account)
        self.assertIsNone(transaction.retailer)
