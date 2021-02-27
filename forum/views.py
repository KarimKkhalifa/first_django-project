from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, CreateView

from .models import Posts, Category
from .forms import PostForm


class HomePosts(ListView):
    model = Posts
    template_name = 'forum/home_posts_list.html'
    context_object_name = 'posts'


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

# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save()
#             return redirect('home')
#     else:
#         form = PostForm()

# def read_more(request, posts_id):
#     post = get_object_or_404(Posts, pk=posts_id)
#     return render(request, 'forum/read_more.html', {'post': post})
