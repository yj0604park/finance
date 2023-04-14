from django import template

register = template.Library()


@register.filter
def print_dollar(value):
    value = round(value, 2)
    if value < 0:
        return f"-${abs(value):.2f}"
    return f"${value:.2f}"
