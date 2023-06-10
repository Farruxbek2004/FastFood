from django.urls import path
from .views import (
    CategoryView,
    CategoryDeleteView,
    CategoryUpdateView,
    CategoryRetriveView,
)

urlpatterns = [
    path('', CategoryView.as_view(), name='category_view'),
    path('<slug:slug>/', CategoryUpdateView.as_view(), name='category_edit'),
    path('<int:pk>/', CategoryRetriveView.as_view(), name='category_read'),
    path('<slug:slug>/', CategoryDeleteView.as_view(), name='category_delete'),
]
