from django import template
register = template.Library()

@register.filter
def category_filter2list(qs, pk):
    return [data for data in qs if data.pk == pk]

@register.filter
def is_done_filter2list(qs):
    return list(filter(lambda data: data.is_done, qs))