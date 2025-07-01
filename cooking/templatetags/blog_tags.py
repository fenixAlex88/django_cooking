from django import template

register = template.Library()


@register.simple_tag
def get_all_categories():
    from cooking.models import Category
    return Category.objects.all()
