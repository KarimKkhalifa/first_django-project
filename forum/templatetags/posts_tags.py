from django import template
from django.db.models import Count
from forum.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('forum/list_categories.html')
def show_categories():
    categories = Category.objects.annotate(cnt=Count('posts')).filter(cnt__gt=0)
    return {'categories': categories}
