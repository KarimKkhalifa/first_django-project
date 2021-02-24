from django.shortcuts import render, get_object_or_404, redirect
from .models import Posts, Category
from .forms import PostForm


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
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Posts.objects.create(**form.cleaned_data)
            return redirect('home')
    else:
        form = PostForm()
        return render(request, 'forum/create_post.html', {'form': form})


def read_more(request, posts_id):
    post = get_object_or_404(Posts, pk=posts_id)
    return render(request, 'forum/read_more.html', {'post': post})
