from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from users.models import User
from .models import Posts
from .serializers import PostResponseSerializer, PostCreateSerializer
from rest_framework.permissions import IsAuthenticated


class PostsViewset(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostResponseSerializer
    permission_classes = [IsAuthenticated]
