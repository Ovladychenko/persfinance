from django import template

register = template.Library()

@register.filter
def currency(value):
    try:
        return "{:,.1f}".format(value)
    except (ValueError, TypeError):
        return value
