from django.utils import formats
from django.template.defaulttags import register
from django.utils.translation import gettext as _

@register.filter
def get_range(count):
    return range(count)

@register.filter
def get(obj, key):
    return obj[key]

@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def truncatesentences(value, arg):
    """
    Truncates a string after a certain number of sentences.
    Argument: Number of sentences to truncate after.
    """
    sentences = value.split('.')
    if len(sentences) > arg:
        return '. '.join(sentences[:arg]) + '...'
    return value

@register.filter
def localize(value):
    """
    If value is a datetime object, localize it using the Russian date format.
    Otherwise, treat it as a string and translate it using _.
    """
    
    if hasattr(value, 'strftime'):
        formatted_date = formats.date_format(value, format='j E Y', use_l10n=True)
        months = {
            'January': 'января',
            'February': 'февраля',
            'March': 'марта',
            'April': 'апреля',
            'May': 'мая',
            'June': 'июня',
            'July': 'июля',
            'August': 'августа',
            'September': 'сентября',
            'October': 'октября',
            'November': 'ноября',
            'December': 'декабря',
        }
        for month_en, month_ru in months.items():
            formatted_date = formatted_date.replace(month_en, month_ru)
        return formatted_date
    return _(value)