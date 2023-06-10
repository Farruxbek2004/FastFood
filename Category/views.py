from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from Category.models import Category
from paginations import CustomPageNumberPagination
from .serializers import CategorySerialzer
from rest_framework.filters import OrderingFilter, SearchFilter


# Create your views here.

# class CategoryView(APIView):
#     def get(self, request):
#         queryset = Category.objects.order_by('-position')
#         serializer = CategorySerialzer(queryset, many=True)
#         return Response(serializer.data)
#
#     permission_classes = [IsAdminUser]
#
#     def post(self, request, *args, **kwargs):
#         serializers = CategorySerialzer(data=request.data)
#         if serializers.is_valid(raise_exception=True):
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.order_by("-id")
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    serializer_class = CategorySerialzer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer
    lookup_field = 'slug'


class CategoryRetriveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer


class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'slug'
