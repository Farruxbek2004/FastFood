from django.urls import path
from .views import CommentView, CommentDetailView

urlpatterns = [
    path('comment/', CommentView.as_view(), name='food-comment'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='food-comment-detil'),
]
