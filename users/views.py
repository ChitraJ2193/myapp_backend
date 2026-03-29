from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)
from .throttles import ScopedAuthThrottle

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedAuthThrottle]
    throttle_scope = "register"


class ThrottledTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedAuthThrottle]
    throttle_scope = "login"


class ThrottledTokenRefreshView(TokenRefreshView):
    throttle_classes = [ScopedAuthThrottle]
    throttle_scope = "login"


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedAuthThrottle]
    throttle_scope = "password_reset"

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].lower()
        message = {"detail": "If an account exists for this email, password reset instructions were sent."}

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(message, status=status.HTTP_200_OK)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        tok = token_generator.make_token(user)
        reset_link = f"{settings.PASSWORD_RESET_FRONTEND_BASE_URL}?uid={uid}&token={tok}"

        if settings.DEBUG:
            message["debug_reset"] = {"uid": uid, "token": tok, "reset_link_hint": reset_link}

        if not settings.DEBUG or getattr(settings, "SEND_EMAIL_IN_DEBUG", False):
            send_mail(
                subject="Password reset",
                message=f"Use this link in the app to reset your password:\n{reset_link}",
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
                recipient_list=[user.email],
                fail_silently=True,
            )

        return Response(message, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedAuthThrottle]
    throttle_scope = "password_reset"

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data["uid"]
        tok = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            uid_int = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_int)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"detail": "Invalid uid."}, status=status.HTTP_400_BAD_REQUEST)

        if not token_generator.check_token(user, tok):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
