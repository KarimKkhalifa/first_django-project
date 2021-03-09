from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .utils import create_comments_tree
from django.db import transaction
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
    comments = Posts.objects.first().comments.all()
    result = create_comments_tree(comments)
    form = CommentForm(request.POST)
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        return render(request, 'forum/read_more.html',
                      {'current_user': current_user, 'post': post, 'comments': result, 'form': form})
    else:
        return render(request, 'forum/read_more.html', {'post': post, 'comments': result, 'form': form})


def create_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.text = form.cleaned_data['text']
        new_comment.content_type = ContentType.objects.get(model='post')
        new_comment.object_id = 1
        new_comment.parent = None
        new_comment.is_child = False
        new_comment.save()
    return redirect('read_more')


@transaction.atomic
def create_child_comment(request):
    user_name = request.POST.get('user')
    current_id = request.POST.get('id')
    text = request.POST.get('text')
    user = User.objects.get(user_name=user_name)
    content_type = ContentType.objects.get(model='post')
    parent = Comments.objects.get(id=int(current_id))
    is_child = False if not parent else True
    Comments.objects.create(
        user=user, text=text, content_type=content_type, object_id=1, parent=parent, is_child=is_child
    )
    comments = Posts.objects.first().comments.all()
    comments_list = create_comments_tree(comments)
    return render(request, 'forum/read_more.html', {'comments': comments_list})


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
