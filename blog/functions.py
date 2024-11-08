from django.template.defaulttags import register

@register.filter
def get_range(count):
    return range(count)

@register.filter
def get(obj, key):
    return obj[key]