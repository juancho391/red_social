from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Likes
from .models import Posts
from .models import Comments
from red_social.utils import upload_image
from users.models import User


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ["id", "post_img", "likes", "description", "publish_date", "id_user"]


class PostCreateSerializer(serializers.ModelSerializer):
    post_img = serializers.ImageField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Posts
        fields = ["post_img", "description", "id_user"]

    def validate(self, attrs):
        if not attrs.get("post_img") and not attrs.get("description"):
            raise serializers.ValidationError(
                "You must provide at least one of the following fields: post_img or description."
            )
        return attrs


class LikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Likes
        fields = ["id_user", "id_post"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["description", "id_post", "id_user"]
