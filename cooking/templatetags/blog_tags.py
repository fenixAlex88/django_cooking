from django import template
from django.db.models import Count, Q
from django.core.cache import cache

register = template.Library()


@register.simple_tag
def get_all_categories():
    from cooking.models import Category
    buttons = cache.get('all_categories')
    if buttons is None:
        buttons = Category.objects.annotate(
                                    cnt=Count('posts', filter=Q(posts__is_published=True))
                                    ).filter(cnt__gt=0)
        cache.set('all_categories', buttons, 60)
    return buttons
