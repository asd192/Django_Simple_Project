import random

from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError

import tours.data as data


def main_view(request):
    """ Главная """

    # забираем доступные ключи словарей
    tours_random = []
    for key in data.tours.keys():
        tours_random.append(key)

    # перемешиваем список ключей
    random.shuffle(tours_random)

    # формируем список словарей
    tours_dict = dict()
    for number in tours_random[:6]:
        tours_dict[number] = data.tours[number]

    about = {
        'title': data.title,
        'subtitle': data.subtitle,
        'description': data.description
    }

    return render(request, 'tours/index.html', {'menu_header': data.departures, 'about': about, 'tours': tours_dict})


def departure_view(request, departure):
    """ Направления """
    if departure not in data.departures.keys():
        return custom_handler404(request, exception=404)

    tours_dict, price, night = dict(), [], []
    for key, value in data.tours.items():
        if data.tours[key]['departure'] == departure:
            tours_dict[key] = value

            # прайс и ночи, от и до
            price.append(int(value['price']))
            night.append(int(value['nights']))

    tours_count = len(tours_dict)

    # окончание тур[а, ов]
    if (int(tours_count) % 10) == 1 and (int(tours_count) % 100) != 11:
        tour_end = ''
    elif 2 <= (int(tours_count) % 10) <= 4 and ((int(tours_count) // 10) % 10) != 1:
        tour_end = 'а'
    else:
        tour_end = 'ов'

    # информация о найденых турах
    fly_from = data.departures[departure].split()[-1]

    info = {
        'count': tours_count,
        'price_min': min(price),
        'price_max': max(price),
        'night_min': min(night),
        'night_max': max(night),
        'tour_end': tour_end
    }

    context = {'menu_header': data.departures,
               'departures': tours_dict,
               'info': info,
               'fly_from': fly_from}

    return render(request, 'tours/departure.html', context=context)


def tour_view(request, id_tour):
    """ Тур """
    tour = data.tours.get(id_tour, False) or False

    if not tour:
        return custom_handler404(request, exception=404)

    if (int(tour['nights']) % 10) == 1 and (int(tour['nights']) % 100) != 11:
        nights_end = 'ь'
    elif 2 <= (int(tour['nights']) % 10) <= 4 and ((int(tour['nights']) // 10) % 10) != 1:
        nights_end = 'и'
    else:
        nights_end = 'ей'

    tour_to_where = data.departures[tour['departure']]

    context = {'menu_header': data.departures,
               'tour': tour,
               'tour_to_where': tour_to_where,
               'nights_end': nights_end}

    return render(request, 'tours/tour.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound(
        '<div align="center" style="margin-top: 10%; color: #29486f;"><div style="background: #eff7ff; \
        padding-top: 30px; padding-bottom: 30px"><h1>Ошибка 404</h1><h3>такой страницы не существует</h3></div><div> \
        <p>Хотите перейти на главную?</p><p><a href="/"><<< Хочу! >>></a></p></div></div>')


def custom_handler500(request):
    return HttpResponseServerError(
        '<div align="center"><p><h1>Ошибка 500</h1></p><p><h2>Ошибка на сервере</h2></p></div>')
