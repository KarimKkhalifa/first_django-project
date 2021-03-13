from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import PostForm, CommentForm
from .models import Posts, Category, Comments
from user.models import User


class HomePosts(ListView):
    model = Posts
    template_name = 'forum/home_posts_list.html'
    context_object_name = 'posts'
    queryset = Posts.objects.select_related('category')
    paginate_by = 2


class PostsByCategory(ListView):
    model = Category
    template_name = 'forum/home_posts_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Posts.objects.filter(category_id=self.kwargs['category_id'])


def read_more(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    form = CommentForm
    if request.user.is_authenticated and request.method == 'GET':
        current_user = User.objects.get(id=request.user.id)
        return render(request, 'forum/read_more.html',
                      {'current_user': current_user, 'form': form, 'post': post})
    elif request.user.is_authenticated and request.method == 'POST':
        form = CommentForm(request.POST)

        url_from = request.POST.get('url_from')
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = Posts.objects.get(pk=post_id)
            obj.author = request.user
            obj.save()
            return redirect(url_from)
    else:
        return render(request, 'forum/read_more.html', {'post': post, })


class CreatePost(CreateView):
    form_class = PostForm
    template_name = 'forum/create_post.html'
    pass


def delete_post(request, pk):
    post = Posts.objects.get(pk=pk)
    post.delete()
    return redirect('home')


def update_post(request, pk):
    post = Posts.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('home')
    context = {'post': post,
               'form': PostForm(instance=post)
               }
    return render(request, 'forum/update_post.html',
                  context)


def delete_comment(request, pk):
    comment = Comments.objects.get(pk=pk)
    comment.delete()
    return redirect('home')
