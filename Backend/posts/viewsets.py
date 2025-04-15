from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from users.models import User
from .models import Posts
from .serializers import PostSerializer, PostCreateSerializer
from rest_framework.permissions import IsAuthenticated
from red_social.utils import upload_image
from rest_framework.response import Response
from rest_framework import status


class PostsViewset(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreateSerializer
        return PostSerializer

    def create(self, request):
        try:
            user = get_object_or_404(User, id=request.data.get("id_user"))
            post_img = request.FILES.get("post_img")

            serializer = PostCreateSerializer(data=request.data)
            if serializer.is_valid():
                post = serializer.save()
            else:
                return Response(
                    {"error": serializer.errors, "message": "Post creation failed"}
                )

            if post_img:
                # Subimos la imagen a s3
                file_url = upload_image(
                    file=post_img,
                    folder="post_images",
                    post_id=post.id,
                    username=user.username,
                )
                # actualizo la url del post
                post.post_img = file_url
                post.save()

            return Response(
                {
                    "message": "Post created successfully",
                    "post": PostSerializer(post).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e), "message": "Post creation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
