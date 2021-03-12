from django.shortcuts import redirect
from django.views.generic import View
from forum.models import Posts, User
from likes.models import PostsLikes


class AddLikeView(View):
    def post(self, request, *args, **kwargs):
        post_id = int(request.POST.get('post_id'))
        user_id = int(request.POST.get('user_id'))
        url_from = request.POST.get('url_from')

        current_user = User.objects.get(id=user_id)
        current_post = Posts.objects.get(id=post_id)

        try:
            post_like_inst = PostsLikes.objects.get(post=current_post, liked_by=current_user)
        except Exception as e:
            post_like = PostsLikes(post=current_post, liked_by=current_user, like=True)

            post_like.save()
        return redirect(url_from)


class RemoveLike(View):
    def post(self, request, *args, **kwargs):
        post_likes_id = int(request.POST.get('post_id'))
        url_from = request.POST.get('url_from')

        post_like = PostsLikes.objects.get(id=post_likes_id)
        post_like.delete()

        return redirect(url_from)
