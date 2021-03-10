from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import PostForm, UserLoginForm, CommentForm
from .models import Posts, Category, User, Comments


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


def read_more(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    form = CommentForm
    if request.user.is_authenticated and request.method == 'GET':
        current_user = User.objects.get(id=request.user.id)
        return render(request, 'forum/read_more.html',
                      {'current_user': current_user, 'form': form, 'post': post})
    elif request.user.is_authenticated and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = Posts.objects.get(pk=post_id)
            obj.author = request.user
            obj.save()
            return redirect('home')
    else:
        return render(request, 'forum/read_more.html', {'post': post, })


class CreatePost(CreateView):
    form_class = PostForm
    template_name = 'forum/create_post.html'
    pass


def delete_post(request, comment_id):
    post = Posts.objects.get(pk=comment_id)
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
