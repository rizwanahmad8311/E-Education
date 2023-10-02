from django import template

register = template.Library()

@register.filter
def percentage(value1,value2):
    if value2 == 0:
        return 0
    else:
        result = (value1/value2)*100
        print(value1,value2)
        return int(result)