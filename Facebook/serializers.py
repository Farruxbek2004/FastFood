from rest_framework import serializers

from . import facebook
from .register import register_social_user


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        try:
            email = user_data['email']
            name = user_data['name']
            return register_social_user(email=email, name=name)
        except Exception as identifier:
            raise serializers.ValidationError('The token  is invalid or expired. Please login again.')
