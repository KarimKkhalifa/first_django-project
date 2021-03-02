from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, CreateView

from .models import Posts, Category
from .forms import PostForm, UserRegisterFrom, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно заригестрировались')
            return redirect('home')

        else:
            messages.error(request, 'Ошибка регистрации')
            return redirect('register')
    else:
        form = UserRegisterFrom()
        return render(request, 'forum/register.html', {'form': form})


# def myregistretion():
# if request.method =='POST':
#     form = MyRegistrationForm(request.POST)
#     if form.is_valid():
#           new_user =User()
#           new_user.user_name = request.POST.get('username')
#           new_user.password = request.POST.get(make_password('password1'))
#           new_user.save()
# else:
#     form = RegistrationForm()


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
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
