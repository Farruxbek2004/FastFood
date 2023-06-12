from django.db import models
from Food.models import Food


# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comment_food')
    body = models.TextField(blank=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='comment')

    class Mete:
        ordering = ['created_at']

    def __str__(self):
        return self.body
