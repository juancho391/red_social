from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status


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
