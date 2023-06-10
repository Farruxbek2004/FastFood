from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from users.managers import CustomUserManager
from datetime import timedelta


# Create your models here.

class User(AbstractUser):
    class UserTypes(models.TextChoices):
        STUDENT = 'student'
        TEACHER = 'teacher'
        SUPERVISOR = 'supervisor'

    user_interestings = [
        ('Technology', 'technology'),
        ('Art', 'art'),
        ('Web', 'web'),
        ('Internet', 'internet'),
    ]
    username = models.CharField(_("username"), max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True)
    age = models.PositiveSmallIntegerField(null=True)
    address = models.CharField(max_length=100, null=True)
    datatime_user = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=55, choices=UserTypes.choices, default=UserTypes.STUDENT)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def fullname(self):
        return self.get_full_name()

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.type = 'admin'
        super(User, self).save(*args, **kwargs)


class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, blank=True,
        related_name="verification_code"
    )
    email = models.EmailField(unique=True, blank=True)
    last_sent_time = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.email

    @property
    def is_expire(self):
        return self.expired_at < self.last_sent_time + timedelta(seconds=30)
