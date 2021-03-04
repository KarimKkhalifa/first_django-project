from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView

from .forms import PostForm, UserLoginForm
from .models import Posts, Category, User


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        User.objects.create(username=username, password=make_password(password))
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Password or username is incorrect')

        return redirect('login')
    else:
        return render(request, 'forum/register.html')


def user_login(request):
    if request.method == 'POST':
        breakpoint()
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Password or username is incorrect')
    else:
        form = UserLoginForm()
        return render(request, 'forum/login.html', {'form': form})


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


class ReadMore(DeleteView):
    model = Posts
    context_object_name = 'post'


class CreatePost(CreateView):
    form_class = PostForm
    template_name = 'forum/create_post.html'
