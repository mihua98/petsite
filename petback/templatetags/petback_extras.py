from django import template
from django.db.models import Count
from petback.models import PetCategory

register = template.Library()

@register.inclusion_tag('petback/inclusions/_categories.html',takes_context=True)
def show_categories(context):
    category_list = PetCategory.objects.annotate(num_lostpets=Count('lostpet')).filter(num_lostpets__gt=0)
    return {
        'category_list':category_list,
    }