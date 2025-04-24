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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreateSerializer
        if self.action == "destroy":
            return PostSerializer
        return PostSerializer

    def create(self, request):
        try:
            user = get_object_or_404(User, id=request.user.id)
            post_img = request.FILES.get("post_img")
            # Añado el id del usuario autenticado a la request
            request.data["id_user"] = user.id
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
                print(file_url)
                # actualizo la url del post
                post.post_img = file_url
                post.save()

                post.refresh_from_db()

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

    def destroy(self, request, **kwargs):
        try:
            user = get_object_or_404(User, id=request.user.id)
            post = get_object_or_404(Posts, id=self.kwargs["pk"])
            # verifico que el post pertenece al usuario
            print(f"user id : {user.id}")
            print(f"post iduser : {post.id_user.id}")
            if post.id_user.id != user.id:
                return Response(
                    {
                        "message": "You cant delete this post because you are not the owner"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            # Elimino la imagen de s3
            if post.post_img:
                pass

            post.delete()

            return Response(
                {
                    "message": "Post deleted succesfully",
                    "post": PostSerializer(post).data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e), "message": "Post Deletion failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
