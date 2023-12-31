from django.urls import path

from .views import (
    FoodAPIview,
    FoodDetilView,
    FoodUpdateView,
    FoodDeleteView,
    LikeDislikeApiview,
    UserLikedFood
)

urlpatterns = [
    path('', FoodAPIview.as_view(), name='food-view'),
    path('update/<int:pk>/', FoodUpdateView.as_view(), name='food-update'),
    path('delete/<int:pk>', FoodDeleteView.as_view(), name='food-delete'),
    path('<int:pk>/like_dislike/', LikeDislikeApiview.as_view(), name='like_or_dislike'),
    path('<slug:slug>', FoodDetilView.as_view(), name='food-detail-view'),
    path('likedfood/', UserLikedFood.as_view(), name='food-detail-view'),
]
