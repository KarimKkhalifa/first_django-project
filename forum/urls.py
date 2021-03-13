from django.urls import path
from .views import *

urlpatterns = [

    path('', HomePosts.as_view(), name='home'),
    path('category/<int:category_id>/', PostsByCategory.as_view(), name='category'),
    path('create/', CreatePost.as_view(), name='create'),
    path('posts/<int:post_id>/', read_more, name='read_more'),
    path('posts/<int:pk>/delete', delete_post, name='delete'),
    path('posts/<int:pk>/update/', update_post, name='update'),
    path('comment/<int:pk>delete/', delete_comment, name='delete_comment'),

]
