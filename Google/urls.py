from django.urls import path
from .views import GoogleSocialAuthView, CheckGoogleVerificationCodeWithParams

urlpatterns = [
    path('google/check-verification-token/', CheckGoogleVerificationCodeWithParams.as_view(),
         name='check-google-token'),
    path('google/', GoogleSocialAuthView.as_view(), name='google_login'),

]
