from django import template

from likes.models import PostsLikes

register = template.Library()


@register.simple_tag(takes_context=True)
def is_liked(context, post_id):
    breakpoint()
    request = context['request']
    try:
        post_likes = PostsLikes.objects.get(post__id=post_id, liked_by=request.user.id).like
    except Exception as e:
        post_likes = False
    return post_likes


@register.simple_tag()
def count_likes(post_id):
    breakpoint()
    return PostsLikes.objects.filter(post__id=post_id, like=True).count()


@register.simple_tag(takes_context=True)
def post_likes_id(context, post_id):
    breakpoint()
    request = context['request']
    return PostsLikes.objects.get(post__id=post_id, liked_by=request.user.id).id
