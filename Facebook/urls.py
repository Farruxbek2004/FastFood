from django.urls import path

from .views import FacebookSocialAuthView, CheckFacebookVerificationCodeWithParams

urlpatterns = [
    path('facebook/check-verification-token/', CheckFacebookVerificationCodeWithParams.as_view(),
         name='check-facebook-token'),
    path('faceobok/', FacebookSocialAuthView.as_view(), name='facebook_login'),
]
