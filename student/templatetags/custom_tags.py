from django import template

register = template.Library()

@register.filter
def percentage(value1,value2):
    result = (value1/value2)*100
    return int(result)