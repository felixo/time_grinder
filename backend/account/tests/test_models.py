import pytest
from django.conf import settings
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_configured_user_can_be_created_with_user_manager():
    user_model = get_user_model()

    user = user_model.objects.create_user(username="tester", password="test-password")

    saved_user = user_model.objects.get(pk=user.pk)
    assert settings.AUTH_USER_MODEL == "account.User"
    assert user_model._meta.label == "account.User"
    assert saved_user.check_password("test-password")
