from django import template
from django.db.models.aggregates import Count

from ..models import Science, Category, Tag

register = template.Library()


@register.inclusion_tag('science/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_sciences=Count('science')).filter(num_sciences__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('science/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_sciences=Count('science')).filter(num_sciences__gt=0)
    return {
        'tag_list': tag_list,
    }


@register.inclusion_tag('science/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Science.objects.dates('created_time', 'month', order='DESC'),
    }
