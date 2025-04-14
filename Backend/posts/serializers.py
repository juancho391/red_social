from rest_framework import serializers
from .models import Likes
from .models import Posts
from .models import Comments


class PostResponseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Posts
        fields = ["id", "post_img", "likes", "description", "publish_date", "id_user"]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ["post_img", "likes", "description", "publish_date", "id_user"]

    def create(self, validated_data):
        if "post_img" not in validated_data and "description" not in validated_data:
            raise serializers.ValidationError(
                "You must provide at least one of the following fields: post_img or description."
            )
        post = Posts.objects.create(**validated_data)
        return post


class LikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Likes
        fields = ["id_user", "id_post"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["description", "id_post", "id_user"]
