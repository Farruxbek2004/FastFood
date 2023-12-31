from django.http import Http404
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Food, LikeDislike
from .serializers import FoodSerializer, LikeDislikeSerializer, UserLikeDislikeSerializer


# Create your views here.


class FoodAPIview(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class FoodDetilView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Food.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return FoodSerializer
        return FoodSerializer


class FoodUpdateView(generics.UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class FoodDeleteView(generics.DestroyAPIView):
    queryset = Food.objects.all()


class LikeDislikeApiview(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LikeDislikeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LikeDislikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        types = serializer.validated_data.get('type')
        user = request.user
        food = Food.objects.filter(id=self.kwargs.get('pk')).first()
        if not food:
            raise Http404
        like_dislike = LikeDislike.objects.filter(food=food, user=user).first()
        if like_dislike and like_dislike == types:
            like_dislike.delete()
        else:
            LikeDislike.objects.update_or_create(food=food, user=user, defaults={'type': types})
            data = {'type': types, 'detail': 'liked_or disliked'}
        return Response(data)


class UserLikedFood(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queyset = LikeDislike.objects.filter(user=request.user)
        serializer = UserLikeDislikeSerializer(queyset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
