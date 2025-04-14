from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from red_social.utils import upload_image
from .models import User
from .serializers import UserSerializer, RegisterUserSerializer, LoginUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
        serializer_class=RegisterUserSerializer,
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
        detail=False,
        methods=["post"],
        url_path="login",
        permission_classes=[AllowAny],
        serializer_class=LoginUserSerializer,
    )
    def login(self, request):
        serializer = LoginUserSerializer(data=request.data)
        user = get_object_or_404(User, username=request.data.get("username"))
        if serializer.is_valid():
            if user.check_password(request.data.get("password")):
                refresh = RefreshToken.for_user(user=user)
                return Response(
                    {
                        "message": "User Login succesfully",
                        "user": UserSerializer(user).data,
                        "token": {
                            "access": str(refresh.access_token),
                            "refresh": str(refresh),
                        },
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"message": "Error", "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True,
        methods=["put"],
        url_path="profile_image",
        permission_classes=[IsAuthenticated],
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
            file_url = upload_image(
                file=profile_img, folder="profile_images", username=user.username
            )
            # actualizar el perfil del usuario
            user.profile_img = file_url
            user.save()

            return Response({"profile_img": file_url, "status": status.HTTP_200_OK})
        except Exception as e:
            return Response(
                {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}
            )
