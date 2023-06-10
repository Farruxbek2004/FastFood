from allauth.socialaccount.adapter import get_adapter
from django.urls import reverse
from datetime import timedelta
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from config import settings
from .models import VerificationCode
from users.serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    SendEmailVerificationCodeSerializer,
    CheckEmailVerificationCodeSerializer
)


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SendEmailVerificationCodeView(APIView):

    @swagger_auto_schema(request_body=SendEmailVerificationCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SendEmailVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = get_random_string(allowed_chars="0123456789", length=6)
        verification_code, _ = (
            VerificationCode.objects.update_or_create(email=email, defaults={"code": code, "is_verified": False})
        )
        verification_code.expired_at = verification_code.last_sent_time + timedelta(seconds=30)
        verification_code.save(update_fields=["expired_at"])
        subject = "Email registration"
        verification_email_url = reverse("check-email")
        message = f"Email tasdiqlash uchun bosing:\n " \
                  f"http://localhost:8000{verification_email_url}?email={email}&code={code}"
        send_mail(
            subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email]
        )
        return Response({"detail": "Successfully sent email verification code."})


class CheckEmailVerificationCodeView(CreateAPIView):
    queryset = VerificationCode.objects.all()
    serializer_class = CheckEmailVerificationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")
        verification_code = self.get_queryset().filter(email=email, is_verified=False).order_by(
            "-last_sent_time").first()
        if verification_code and verification_code.code != code and not verification_code.is_expire:
            raise ValidationError("Verification code invalid.")
        verification_code.is_verified = True
        verification_code.save(update_fields=["is_verified"])
        return Response({"detail": "Verification  code is verified."})


class CheckEmailVerificationCodeWithParams(APIView):
    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")
        code = request.query_params.get("code")
        verification_code = VerificationCode.objects.filter(email=email, is_verified=False).order_by(
            "-last_sent_time").first()
        if verification_code and verification_code.code != code:
            raise ValidationError("Verification code invalid.")
        verification_code.is_verified = True
        verification_code.save(update_fields=["is_verified"])
        return Response({"detail": "Verification  code is verified."})
