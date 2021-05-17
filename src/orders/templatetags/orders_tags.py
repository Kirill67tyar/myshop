from transliterate import translit, get_available_language_codes

from django import template

register = template.Library()


@register.filter
def translit_from_ru_to_eng(word):
    return translit(u"{}".format(word), 'ru', reversed=True)

# transliterate docs:
# https://pypi.org/project/transliterate/
