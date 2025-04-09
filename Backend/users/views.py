from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.conf import settings
import boto3


# Configuramos el cliente de s3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data.get("username"))
            user.set_password(request.data.get("password"))
            user.save()

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "User Resgister succesfully",
                    "user": serializer.data,
                }
            )

        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Error",
                "error": serializer.errors,
            }
        )


class Login(APIView):
    def post(self, request):
        # user = User.objects.get(username=request.data.get("username"))
        user = get_object_or_404(User, username=request.data.get("username"))
        if user.check_password(request.data.get("password")):
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "message": "User Login succesfully",
                    "user": UserSerializer(user).data,
                }
            )
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "password invalid",
            }
        )


# Endpoint para el crud la descripcion del perfil del usuario
class ProfileDescription(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        return Response({"description": user.description})

    def put(self, request, pk):
        user = get_object_or_404(User, id=pk)
        description = request.data.get("description")
        if not description:
            return Response(
                {
                    "error": "Description has not been provided",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
        user.description = description
        user.save()
        return Response(
            {
                "status": status.HTTP_200_OK,
                "user": UserSerializer(user).data,
                "message": "Description has been updated",
            }
        )

    def delete(self, request, pk):

        user = get_object_or_404(User, id=pk)
        user.description = None
        user.save()
        return Response(
            {
                "status": status.HTTP_200_OK,
                "user": UserSerializer(user).data,
                "message": "Description has been deleted",
            }
        )


# Endpoint para cargar la imagen del perfil del usuario
class ProfileImage(APIView):
    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)

            profile_img = request.FILES.get("profile_img")
            if not profile_img:
                return Response(
                    {
                        "error": "Image has not been provide",
                        "status": status.HTTP_400_BAD_REQUEST,
                    }
                )
            # subir la imagen a s3
            file_name = f"{user.username}"
            s3_client.upload_fileobj(
                profile_img,
                settings.AWS_STORAGE_BUCKET_NAME,
                f"profile_images/{file_name}",
                ExtraArgs={"ContentType": "image/png"},
            )

            # generar la url
            file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/profile_images/{file_name}"

            # actualizar el perfil del usuario
            user.profile_img = file_url
            user.save()

            return Response({"profile_img": file_url, "status": status.HTTP_200_OK})

        except User.DoesNotExist:
            return Response(
                {
                    "error": "user not found",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
        except Exception as e:
            return Response(
                {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}
            )
