import datetime

from django import template

from money.models import CurrencyType

register = template.Library()


@register.filter
def print_dollar(value):
    if not value and value != 0:
        return value

    value = round(value, 2)
    if value < 0:
        return f"&#8209;${abs(value):,.2f}"
    return f"${abs(value):,.2f}"


@register.filter
def print_krw(value):
    if not value and value != 0:
        return value

    value = round(value)
    if value < 0:
        return f"&#8209;₩{abs(value):,.0f}"
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


@register.filter
def get_value(value, arg):
    return value[arg]


@register.filter
def update_month(dictionary, value):
    dictionary["month"] = value
    return dictionary


@register.filter
def update_page(dictionary, value):
    dictionary["page"] = value
    return dictionary


@register.filter
def update_dictionary(dictionary, key_value):
    key, value = key_value.split("=")
    dictionary[key] = value
    return dictionary


@register.filter
def print_argument(dictionary):
    arguments = [f"{k}={v}" for k, v in dictionary.items()]
    return f"?{'&'.join(arguments)}"


@register.filter
def days_ago(date):
    try:
        diff = datetime.datetime.today().replace(tzinfo=None) - date.replace(
            tzinfo=None
        )
    except:
        diff = datetime.datetime.today().date() - date
    if diff < datetime.timedelta(days=1):
        return f"<1 day"
    else:
        return f"{diff.days} days"
