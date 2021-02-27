from django.urls import path
from .views import *

urlpatterns = [
    # path('', views.index, name='home'),
    path('', HomePosts.as_view(), name='home'),
    # path('category/<int:category_id>/', get_category, name='category'),
    path('category/<int:category_id>/', PostsByCategory.as_view(), name='category'),

    # path('create/', create_post, name='create'),
    path('create/', CreatePost.as_view(), name='create'),

    path('posts/<int:pk>/', ReadMore.as_view(), name='read_more')

    # path('posts/<int:posts_id>/', read_more, name='read_more')

]
