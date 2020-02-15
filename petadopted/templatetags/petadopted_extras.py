from django import template
from django.db.models.aggregates import Count

from ..models import Petadopted, Category, Tag

register = template.Library()


@register.inclusion_tag('petadopted/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_petadopteds=Count('petadopted')).filter(num_petadopteds__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('petadopted/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_petadopteds=Count('petadopted')).filter(num_petadopteds__gt=0)
    return {
        'tag_list': tag_list,
    }


@register.inclusion_tag('petadopted/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Petadopted.objects.dates('created_time', 'month', order='DESC'),
    }

