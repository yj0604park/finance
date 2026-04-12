"""
Tests for money app REST API endpoints.

Covers BankViewSet (list, retrieve) and basic authentication requirements.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from money.models.accounts import Bank


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


# ---------------------------------------------------------------------------
# BankViewSet
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestBankViewSetList:
    """Tests for GET /api/money/ (list endpoint)."""

    def test_list_requires_authentication(self, api_client):
        """Unauthenticated requests must be rejected."""
        url = reverse("api:bank-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_returns_empty_for_no_banks(self, authenticated_client):
        url = reverse("api:bank-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # SimpleRouter (used when DEBUG=False in test settings) returns a plain
        # list; DefaultRouter wraps it in {"results": [...], "count": N}.
        data = response.data
        items = data["results"] if isinstance(data, dict) else data
        assert items == []

    def test_list_returns_banks(self, authenticated_client, db):
        Bank.objects.create(name="Alpha Bank")
        Bank.objects.create(name="Beta Bank")
        url = reverse("api:bank-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        items = data["results"] if isinstance(data, dict) else data
        names = [item["name"] for item in items]
        assert "Alpha Bank" in names
        assert "Beta Bank" in names

    def test_list_response_structure(self, authenticated_client, bank):
        url = reverse("api:bank-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        items = data["results"] if isinstance(data, dict) else data
        assert len(items) == 1
        assert "name" in items[0]

    def test_list_count(self, authenticated_client, db):
        for i in range(5):
            Bank.objects.create(name=f"Bank {i}")
        url = reverse("api:bank-list")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        if isinstance(data, dict):
            assert data["count"] == 5
        else:
            assert len(data) == 5


@pytest.mark.django_db
class TestBankViewSetRetrieve:
    """Tests for GET /api/money/{id}/ (detail endpoint)."""

    def test_retrieve_requires_authentication(self, api_client, bank):
        url = reverse("api:bank-detail", kwargs={"pk": bank.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_existing_bank(self, authenticated_client, bank):
        url = reverse("api:bank-detail", kwargs={"pk": bank.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == bank.name

    def test_retrieve_nonexistent_bank(self, authenticated_client):
        url = reverse("api:bank-detail", kwargs={"pk": 99999})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_response_fields(self, authenticated_client, bank):
        url = reverse("api:bank-detail", kwargs={"pk": bank.pk})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "name" in response.data

    def test_no_post_allowed(self, authenticated_client):
        """BankViewSet is read-only; POST must be rejected."""
        url = reverse("api:bank-list")
        response = authenticated_client.post(url, data={"name": "New Bank"})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_no_put_allowed(self, authenticated_client, bank):
        """BankViewSet is read-only; PUT must be rejected."""
        url = reverse("api:bank-detail", kwargs={"pk": bank.pk})
        response = authenticated_client.put(url, data={"name": "Renamed Bank"})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_no_delete_allowed(self, authenticated_client, bank):
        """BankViewSet is read-only; DELETE must be rejected."""
        url = reverse("api:bank-detail", kwargs={"pk": bank.pk})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


# ---------------------------------------------------------------------------
# BankSerializer field tests
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestBankSerializer:
    def test_serializer_exposes_name(self, authenticated_client, bank):
        url = reverse("api:bank-detail", kwargs={"pk": bank.pk})
        response = authenticated_client.get(url)
        assert response.data["name"] == "Test Bank"
