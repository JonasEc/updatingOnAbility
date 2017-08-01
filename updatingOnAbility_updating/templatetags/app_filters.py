from django import template
register = template.Library()


@register.filter(name='negate')
def negate(value):
    return abs(value)
