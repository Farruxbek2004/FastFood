# Create your models here.
from django.db import models


class Facebook(models.Model):
    class ProviderTypes(models.TextChoices):
        FACEBOOK = "facebook"

    # user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="social_account", null=True)
    social_account = models.CharField(max_length=50, choices=ProviderTypes.choices)