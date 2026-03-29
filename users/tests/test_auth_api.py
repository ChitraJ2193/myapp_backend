import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestAuthEndpoints:
    def setup_method(self):
        self.client = APIClient()

    def test_register_and_login(self):
        reg_url = reverse("register")
        payload = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "testpass123",
        }
        r = self.client.post(reg_url, payload, format="json")
        assert r.status_code == status.HTTP_201_CREATED

        login_url = reverse("login")
        login_r = self.client.post(
            login_url,
            {"email": "newuser@example.com", "password": "testpass123"},
            format="json",
        )
        assert login_r.status_code == status.HTTP_200_OK
        assert "access" in login_r.data
        assert "refresh" in login_r.data
