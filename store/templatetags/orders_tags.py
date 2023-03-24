from django import template
from math import floor


register = template.Library()


@register.simple_tag
def get_order_status(status):
    if status == "COMPLETED":
        return "success"
    else:
        return "info"

