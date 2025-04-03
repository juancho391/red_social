from rest_framework import serializers
from models import Likes
from models import Posts
from models import Comments


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Posts
        fields = ["id", "post_img", "likes", "description", "publish_date", "id_user"]


class LikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Likes
        fields = ["id_user", "id_post"]


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comments
        fields = ["id", "description", "id_post", "id_user"]
