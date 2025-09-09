from django import template

register = template.Library()

BAD_WORDS = ['дурак', 'глупый', 'плохой', 'редиска']  # список нежелательных слов

@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        return value

    text = value
    for bad_word in BAD_WORDS:
        replace_str = bad_word[0] + "*" * (len(bad_word) - 1)
        text = text.replace(bad_word, replace_str)
        text = text.replace(bad_word.capitalize(), replace_str.capitalize())
    return text