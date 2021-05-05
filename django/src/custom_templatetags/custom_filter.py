from django import template
register = template.Library()

@register.filter
def category_filter(qs, category_name):
    return qs.filter(category__name=category_name)

@register.filter
def is_done_filter(qs):
    return qs.filter(is_done=True)