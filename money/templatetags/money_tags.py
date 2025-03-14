import copy
import datetime

from django import template

from money.choices import CurrencyType

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

    if currency == CurrencyType.USD:
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
    result = copy.deepcopy(dictionary)
    result["month"] = value
    return result


@register.filter
def update_page(dictionary, value):
    result = copy.deepcopy(dictionary)
    result["page"] = value
    return result


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
    if date is None:
        return "Unk"
    try:
        diff = datetime.datetime.today().replace(tzinfo=None) - date.replace(
            tzinfo=None
        )
    # trunk-ignore(pylint/W0718)
    except Exception:
        diff = datetime.datetime.today().date() - date

    if diff < datetime.timedelta(days=1):
        return "<1 day"

    return f"{diff.days} days"
