from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('category/<int:category_id>/', views.get_category, name='category'),
    path('create/', views.create_post, name='create'),
    path('posts/<int:posts_id>/', views.read_more, name='read_more')

]
