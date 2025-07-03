from django import template
from django.db.models import Count, Q

register = template.Library()


@register.simple_tag
def get_all_categories():
    from cooking.models import Category
    return Category.objects.annotate(
                                    cnt=Count('posts', filter=Q(posts__is_published=True))
                                    ).filter(cnt__gt=0)
