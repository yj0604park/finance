from django import template

from money.models import CurrencyType

register = template.Library()


@register.filter
def print_dollar(value):
    if not value and value != 0:
        return value

    value = round(value, 2)
    if value < 0:
        return f"-${abs(value):,.2f}"
    return f"${abs(value):,.2f}"


@register.filter
def print_krw(value):
    if not value:
        return value

    value = round(value)
    if value < 0:
        return f"-₩{abs(value):,.0f}"
    return f"₩{abs(value):,.0f}"


@register.filter
def print_currency(value, currency):
    currency = currency.upper()
    if currency == CurrencyType.KRW:
        return print_krw(value)
    elif currency == CurrencyType.USD:
        return print_dollar(value)
    return value


@register.filter
def abs_filter(value):
    return abs(value)


@register.filter
def add_float(value1, value2):
    return value1 + value2


@register.filter
def multiply(value, arg):
    return value * arg
