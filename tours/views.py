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

    about = {'title': data.title, 'subtitle': data.subtitle, 'description': data.description}

    return render(request, 'index.html', {'menu_header': data.departures, 'about': about, 'tours': tours_dict})


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
    if str(tours_count)[-1] in ('2', '3', '4'):
        tour_end = 'а'
    elif str(tours_count)[-1] in '1':
        tour_end = ''
    else:
        tour_end = 'ов'

    # информация о найденых турах
    fly_from = data.departures[departure].split()[-1]
    info = {'count': tours_count, 'price_min': min(price), 'price_max': max(price), 'night_min': min(night),
            'night_max': max(night), 'tour_end': tour_end}

    return render(request, 'departure.html', {'menu_header': data.departures, 'departures': tours_dict, 'info': info,
                                              'fly_from': fly_from})


def tour_view(request, id):
    """ Тур """
    tour = data.tours.get(id, False)
    if not tour:
        return custom_handler404(request, exception=404)
    return render(request, 'tour.html', {'menu_header': data.departures, 'tour': tour})


def custom_handler404(request, exception):
    return HttpResponseNotFound(
        '<div align="center" style="margin-top: 10%; color: #29486f;"><div style="background: #eff7ff; \
        padding-top: 30px; padding-bottom: 30px"><h1>Ошибка 404</h1><h3>такой страницы не существует</h3></div><div> \
        <p>Хотите перейти на главную?</p><p><a href="/"><<< Хочу! >>></a></p></div></div>')


def custom_handler500(request):
    return HttpResponseServerError(
        '<div align="center"><p><h1>Ошибка 500</h1></p><p><h2>Ошибка на сервере</h2></p></div>')
