from django.db import models


class Google(models.Model):
    class ProviderTypes(models.TextChoices):
        GOOGLE = "google"

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="social_account", null=True)
    social_account = models.CharField(max_length=50, choices=ProviderTypes.choices)