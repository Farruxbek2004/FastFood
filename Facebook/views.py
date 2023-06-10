from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import FacebookSocialAuthSerializer
from rest_framework.views import APIView
from users.models import VerificationCode
from rest_framework.exceptions import ValidationError


# Create your views here.

class CheckFacebookVerificationCodeWithParams(APIView):
    def get(self, request, *args, **kwargs):
        token = request.query_params.get("code")
        verification_token = VerificationCode.objects.filter(token=token).order_by(
            "-last_sent_time").first()
        if verification_token and verification_token.code != token:
            raise ValidationError("Verification token invalid.")
        verification_token.is_verified = True
        verification_token.save(update_fields=["is_verified"])
        return Response({"detail": "Verification  token is verified."})


class FacebookSocialAuthView(GenericAPIView):
    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an access_token as from Facebook to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data['auth_token']
        return Response(data, status=status.HTTP_200_OK)
