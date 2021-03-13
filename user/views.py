from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from forum.models import Posts
from user.forms import UserLoginForm
from .models import User


def get_user_profile(request):
    current_user = User.objects.get(username=request.user)
    posts = Posts.objects.filter(author=current_user)
    return render(request, 'user/user_profile.html', {'current_user': current_user, 'posts': posts})


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
        return render(request, 'user/register.html')


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
        return render(request, 'user/login.html', {'form': form})


def delete_user_account(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('home')
