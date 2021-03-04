from django.urls import path
from .views import *

urlpatterns = [

    path('', HomePosts.as_view(), name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('category/<int:category_id>/', PostsByCategory.as_view(), name='category'),
    path('create/', CreatePost.as_view(), name='create'),
    path('posts/<int:pk>/', ReadMore.as_view(), name='read_more'),
]
