from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtracts `arg` from `value`."""
    return value - arg
