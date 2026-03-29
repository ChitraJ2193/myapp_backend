from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
    ThrottledTokenObtainPairView,
    ThrottledTokenRefreshView,
    UserProfileView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", ThrottledTokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", ThrottledTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/profile/", UserProfileView.as_view(), name="profile"),
    path("auth/password/reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("auth/password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
