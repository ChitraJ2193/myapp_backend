import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()
gen = PasswordResetTokenGenerator()


@pytest.mark.django_db
def test_password_reset_flow():
    client = APIClient()
    user = User.objects.create_user(
        email="reset@example.com",
        username="resetuser",
        password="oldpass12345",
    )
    r = client.post(reverse("password_reset"), {"email": user.email}, format="json")
    assert r.status_code == status.HTTP_200_OK

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = gen.make_token(user)
    confirm = client.post(
        reverse("password_reset_confirm"),
        {"uid": uid, "token": token, "new_password": "newpass12345"},
        format="json",
    )
    assert confirm.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password("newpass12345")
