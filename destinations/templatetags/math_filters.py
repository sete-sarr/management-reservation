from django import template

register = template.Library()


@register.filter
def divide(value, divisor):
    """Divide one value by another."""
    try:
        return float(value) / float(divisor)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0


@register.filter
def multiply(value, multiplier):
    """Multiply a value."""
    try:
        return float(value) * float(multiplier)
    except (ValueError, TypeError):
        return 0
