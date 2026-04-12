"""
Tests for finance/users/api_views.py:
  - api_login_view  (POST /api/auth/login/)
  - api_logout_view (POST /api/auth/logout/)
  - api_me_view     (GET  /api/auth/me/)
"""

import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()

LOGIN_URL = "/api/auth/login/"
LOGOUT_URL = "/api/auth/logout/"
ME_URL = "/api/auth/me/"


def _post_json(client, url, data):
    return client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )


# ---------------------------------------------------------------------------
# api_me_view  GET /api/auth/me/
# ---------------------------------------------------------------------------
class MeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="secret123")
        self.client = Client()

    def test_me_unauthenticated_returns_401(self):
        """미인증 상태에서 me 엔드포인트는 401을 반환해야 한다."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.content)
        self.assertFalse(data["authenticated"])

    def test_me_authenticated_returns_username(self):
        """인증 후 me 엔드포인트는 사용자명과 authenticated=true를 반환해야 한다."""
        self.client.force_login(self.user)
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data["authenticated"])
        self.assertEqual(data["username"], "alice")

    def test_me_only_allows_get(self):
        """me 엔드포인트는 POST를 허용하지 않아야 한다."""
        self.client.force_login(self.user)
        res = self.client.post(ME_URL)
        self.assertEqual(res.status_code, 405)


# ---------------------------------------------------------------------------
# api_login_view  POST /api/auth/login/
# ---------------------------------------------------------------------------
class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="pass1234")
        self.client = Client()

    def test_valid_credentials_return_200_and_authenticated(self):
        """올바른 자격증명은 200과 authenticated=true를 반환해야 한다."""
        res = _post_json(self.client, LOGIN_URL, {"username": "bob", "password": "pass1234"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data["authenticated"])
        self.assertEqual(data["username"], "bob")

    def test_valid_login_creates_session(self):
        """로그인 후 me 엔드포인트에 접근할 수 있어야 한다 (세션 쿠키 확인)."""
        _post_json(self.client, LOGIN_URL, {"username": "bob", "password": "pass1234"})
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(data["authenticated"])

    def test_wrong_password_returns_401(self):
        """잘못된 비밀번호는 401을 반환해야 한다."""
        res = _post_json(self.client, LOGIN_URL, {"username": "bob", "password": "wrong"})
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.content)
        self.assertIn("error", data)

    def test_nonexistent_user_returns_401(self):
        """존재하지 않는 사용자는 401을 반환해야 한다."""
        res = _post_json(self.client, LOGIN_URL, {"username": "nobody", "password": "pass"})
        self.assertEqual(res.status_code, 401)

    def test_missing_username_returns_400(self):
        """username 누락 시 400을 반환해야 한다."""
        res = _post_json(self.client, LOGIN_URL, {"password": "pass1234"})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.content)
        self.assertIn("error", data)

    def test_missing_password_returns_400(self):
        """password 누락 시 400을 반환해야 한다."""
        res = _post_json(self.client, LOGIN_URL, {"username": "bob"})
        self.assertEqual(res.status_code, 400)

    def test_empty_username_returns_400(self):
        """빈 문자열 username은 400을 반환해야 한다 (공백 trim 포함)."""
        res = _post_json(self.client, LOGIN_URL, {"username": "   ", "password": "pass1234"})
        self.assertEqual(res.status_code, 400)

    def test_malformed_json_returns_400(self):
        """잘못된 JSON 요청은 400을 반환해야 한다."""
        res = self.client.post(
            LOGIN_URL,
            data="not-valid-json",
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)

    def test_get_method_not_allowed(self):
        """GET 메서드는 허용되지 않아야 한다."""
        res = self.client.get(LOGIN_URL)
        self.assertEqual(res.status_code, 405)

    def test_username_is_stripped(self):
        """username 주변 공백은 trim되어야 한다."""
        res = _post_json(self.client, LOGIN_URL, {"username": "  bob  ", "password": "pass1234"})
        self.assertEqual(res.status_code, 200)


# ---------------------------------------------------------------------------
# api_logout_view  POST /api/auth/logout/
# ---------------------------------------------------------------------------
class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="carol", password="secret")
        self.client = Client()

    def test_logout_from_authenticated_session(self):
        """로그인 상태에서 로그아웃 후 me는 401을 반환해야 한다."""
        self.client.force_login(self.user)
        res = self.client.post(LOGOUT_URL)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertFalse(data["authenticated"])

        # 로그아웃 후 me 요청
        me_res = self.client.get(ME_URL)
        self.assertEqual(me_res.status_code, 401)

    def test_logout_from_unauthenticated_is_safe(self):
        """미인증 상태에서 로그아웃을 해도 오류가 발생하지 않아야 한다."""
        res = self.client.post(LOGOUT_URL)
        self.assertEqual(res.status_code, 200)

    def test_logout_allows_get(self):
        """logout은 GET도 허용한다 (편의)."""
        self.client.force_login(self.user)
        res = self.client.get(LOGOUT_URL)
        self.assertEqual(res.status_code, 200)
