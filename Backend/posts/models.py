from django.db import models
from users.models import User


class Posts(models.Model):
    post_img = models.CharField(max_length=100, null=True)
    no_likes = models.IntegerField(default=0)
    description = models.CharField(max_length=500, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"{self.id_user} - {self.description}"


class Likes(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    id_post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.id_user} - {self.id_post}"


class Comments(models.Model):
    description = models.TextField(max_length=100)
    id_post = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name="comments"
    )
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.id_user} - {self.description}"


# user.posts.all()
# user.likes.all()
# user.comments.all()
# post.likes.all()
# post.comments.all()
