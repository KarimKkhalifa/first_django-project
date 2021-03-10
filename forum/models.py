from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class Posts(models.Model):
    title = models.CharField('Название', max_length=150)
    content = models.TextField('Тема', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    views = models.ImageField(default=0)
    author = models.ForeignKey('User', default=1, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('read_more', kwargs={"post_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=50, db_index=True,
                             verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']


class User(AbstractUser):
    username = models.CharField('username', max_length=50, unique=True)
    password = models.CharField('password', max_length=50)

    def __str__(self):
        return self.username


class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name='Post', blank=True, null=True,
                             related_name='comments_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', blank=True, null=True)
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now=True)


