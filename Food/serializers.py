from rest_framework import serializers

from .models import Food, LikeDislike


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            'name',
            'slug',
            'food_price',
            'composition',
            'image',
            'category',
            'likes',
            'dislike',
        ]
        read_only_fields = ('id', 'price')


class LikeDislikeSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=LikeDislike.Textchoices.choices)


class UserLikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = (
            'food_name',
        )


