from django import template
register = template.Library()

@register.filter
def category_filter2list(qs, pk):
    return [data for data in qs if data.pk == pk]

@register.filter
def lookup(data, key, default=''):
    return data.get(key, default)
