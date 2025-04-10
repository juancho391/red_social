from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer, RegisterUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action
from django.conf import settings
import boto3


# Configuramos el cliente de s3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
        permission_classes=[AllowAny],
    )
    def register(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User register successfully",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=["post"], url_path="login", permission_classes=[AllowAny]
    )
    def login(self, request):
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
                "message": "invalid credentials",
            }
        )

    # @action(
    #     detail=True,
    #     methods=["put", "get"],
    #     permission_classes=[AllowAny],
    #     url_path="description",
    # )
    # def update_description(self, request, pk=None):
    #     user = self.get_object()
    #     user.description = request.data.get("description")
    #     user.save()
    #     return Response({"message": "Description updated."})

    @action(
        detail=True,
        methods=["put"],
        url_path="profile_image",
        permission_classes=[AllowAny],
    )
    def upload_profile_image(self, request, pk):
        try:
            user = get_object_or_404(User, id=pk)

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
        except Exception as e:
            return Response(
                {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}
            )
