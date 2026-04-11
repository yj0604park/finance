import pytest
from django.urls import reverse


def test_swagger_accessible_by_admin(admin_client):
    # URL name defined in config/urls.py as "swagger-ui"
    url = reverse("swagger-ui")
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_swagger_ui_not_accessible_by_normal_user(client):
    url = reverse("swagger-ui")
    response = client.get(url)
    # Unauthenticated users are redirected to the login page
    assert response.status_code in [302, 403]


def test_api_schema_generated_successfully(admin_client):
    # URL name defined in config/urls.py as "schema"
    url = reverse("schema")
    response = admin_client.get(url)
    assert response.status_code == 200
