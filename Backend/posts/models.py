from django.db import models
from users.models import User


class Posts(models.Model):
    post_img = models.CharField(max_length=100, null=True)
    no_likes = models.IntegerField(default=0)
    description = models.CharField(max_length=500, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Likes(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_post = models.ForeignKey(Posts, on_delete=models.CASCADE)


class Comments(models.Model):
    description = models.TextField(max_length=100)
    id_post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
