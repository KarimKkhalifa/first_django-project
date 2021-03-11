from django.db import models
from forum.models import Posts, User


class PostsLikes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name='Post in the blog')
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Liked by')
    like = models.BooleanField(default=False, verbose_name='Like')
