from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "description",
            "profile_img",
        ]


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "birth_date",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_username(self, value):
        if value.isdigit():
            raise serializers.ValidationError("Username can't be only numbers.")
        return value


class UpdateUserDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "description",
        ]
