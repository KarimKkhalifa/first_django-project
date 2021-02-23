from django.shortcuts import render
from .models import Posts, Category


def index(request):
    posts = Posts.objects.all()
    categories = Category.objects.all()
    context = {'title': 'The main page of the site',
               'posts': posts,
               'categories': categories}
    return render(request, 'forum/index.html', context)


def get_category(request, category_id):
    posts = Posts.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    return render(request, 'forum/category.html', {'posts': posts,
                                                   'categories': categories,
                                                   'category': category})


def create_post(request):
    return render(request, 'forum/create_post.html')
