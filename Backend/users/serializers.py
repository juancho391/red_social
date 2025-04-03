from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "description",
            "profile_img",
        ]

    def validate_username(self, value):
        # Verificar que el username tenga al menos una letra
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("The username has to contain letters.")
        return value
