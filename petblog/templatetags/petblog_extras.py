from django import template
from django.db.models.aggregates import Count

from ..models import Post, Category, Tag
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('petblog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=3):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num]
    }


@register.inclusion_tag('petblog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('petblog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }


@register.inclusion_tag('petblog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


@register.inclusion_tag('petblog/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }


@register.inclusion_tag('petblog/inclusions/_comments.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all().order_by('created_time')
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }
