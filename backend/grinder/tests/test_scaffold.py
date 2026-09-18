import pytest
from django.contrib.auth import get_user_model


def test_health(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_custom_user_persists():
    user_model = get_user_model()
    user = user_model.objects.create_user(username="tester", password="test-password")

    saved_user = user_model.objects.get(pk=user.pk)
    assert saved_user.check_password("test-password")
    assert user_model._meta.label == "grinder.User"


def test_admin_login(client):
    assert client.get("/admin/login/").status_code == 200
