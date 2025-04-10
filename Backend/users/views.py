from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import User
from .serializers import (
    UserSerializer,
    RegisterUserSerializer,
    UpdateUserDescriptionSerializer,
)
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


# Endpoint para el crud la descripcion del perfil del usuario
class ProfileDescription(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        return Response({"description": user.description})

    def patch(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = UpdateUserDescriptionSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "user": UserSerializer(user).data,
                    "message": "Description has been updated",
                }
            )
        return Response(
            {
                "error": "Description has not been provided",
                "status": status.HTTP_400_BAD_REQUEST,
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
