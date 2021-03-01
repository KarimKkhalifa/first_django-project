from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, CreateView

from .models import Posts, Category
from .forms import PostForm


class HomePosts(ListView):
    model = Posts
    template_name = 'forum/home_posts_list.html'
    context_object_name = 'posts'
    queryset = Posts.objects.select_related('category')


class PostsByCategory(ListView):
    model = Category
    template_name = 'forum/home_posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Posts.objects.filter(category_id=self.kwargs['category_id'])


class ReadMore(DeleteView):
    model = Posts
    context_object_name = 'post'


class CreatePost(CreateView):
    form_class = PostForm
    template_name = 'forum/create_post.html'


