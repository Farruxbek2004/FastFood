from django.shortcuts import render
from rest_framework import generics
from .serializers import CommentSerializer
from .models import Comment


# Create your views here.


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
