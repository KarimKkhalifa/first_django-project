from django.contrib import admin
from .models import Posts, Category


class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','content', 'created_at', 'update_at')


admin.site.register(Posts)
admin.site.register(Category)

