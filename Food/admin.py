from django.contrib import admin
from .models import Food,  LikeDislike


# Register your models here.


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(LikeDislike)
class LIkeDislike(admin.ModelAdmin):
    list_display = ['user', 'food', 'type']


