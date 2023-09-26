from django import template


register = template.Library()


CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
}


@register.filter()
def currency(value, code='rub'):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   postfix = CURRENCIES_SYMBOLS[code]

   return f'{value} {postfix}'

censored_words = ['ipsum', 'sit']
@register.filter()
def censor(value):
    if isinstance(value, str):
        for word in censored_words:
            letters = list(word)
            for i in range(1, len(letters)):
                letters[i] = '*'
            censored_word = ''.join(letters)
            value = value.replace(word, censored_word, -1)
    return value