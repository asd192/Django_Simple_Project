from typing import Union

from django import template

register = template.Library()


@register.filter()
def ru_pluralize(number: Union[int, str], arg: str = 'ночь, ночи, ночей'):
    nominative_singular, nominative_plural, genitive_plural = arg.split(', ')
    number = abs(int(number))

    if (number % 10) == 1 and number % 100 != 11:
        return f'{number} {nominative_singular}'
    elif 2 <= number % 10 <= 4 and number // 10 % 10 != 1:
        return f'{number} {nominative_plural}'
    else:
        return f'{number} {genitive_plural}'


@register.filter()
def hotel_stars(number: Union[int, str], arg: str = '★☆☆☆☆, ★★☆☆☆, ★★★☆☆, ★★★★☆, ★★★★★'):
    one, two, three, four, five = arg.split(', ')
    number = abs(int(number))

    if number == 1:
        return one
    elif number == 2:
        return two
    elif number == 3:
        return three
    elif number == 4:
        return four
    elif number == 5:
        return five
    return '☆☆☆☆☆'
