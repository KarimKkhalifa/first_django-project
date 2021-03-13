from django.contrib import admin
from .models import Posts, Category,  Comments


class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'update_at')


admin.site.register(Posts)
admin.site.register(Category)
admin.site.register(Comments)

