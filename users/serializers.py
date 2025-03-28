from rest_framework import serializers
from models import User


class UserSerializer(serializers.ModelSerializer):
    description = serializers.TextField(required=False)
    profile_image = serializers.CharField(required=False)
    id = serializers.IntegerField(read_only=True)

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
