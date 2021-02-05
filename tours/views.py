import random

from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError

from tours.data import *


def MainView(request):
    """ Главная """

    # забираем доступные ключи словарей
    tours_random = []
    for key in tours.keys():
        tours_random.append(key)

    # перемешиваем список ключей
    random.shuffle(tours_random)

    # формируем список словарей
    tours_dict = dict()
    for number in tours_random[:6]:
        tours_dict[number] = tours[number]

    about = {'title': title, 'subtitle': subtitle, 'description': description}

    return render(request, 'index.html', {'menu_header': departures, 'about': about, 'tours': tours_dict})


def DepartureView(request, departure):
    """ Направления """
    price_min, price_max = 1e+8, -1e+8
    night_min, night_max = 1e+8, -1e+8
    tours_dict = dict()
    for key, value in tours.items():
        if tours[key]['departure'] == departure:
            tours_dict[key] = value

            price = int(value['price'])
            if price > price_max:
                price_max = price
            if price < price_min:
                price_min = price

            night = int(value['nights'])
            if night > night_max:
                night_max = night
            if night < night_min:
                night_min = night

    tours_count = len(tours_dict)

    # окончание тур[а, ов]
    if str(tours_count)[-1] in ('2', '3', '4'):
        tour_end = 'а'
    elif str(tours_count)[-1] in '1':
        tour_end = ''
    else:
        tour_end = 'ов'

    # информация о найденых турах
    info = {'count': tours_count, 'price_min': price_min, 'price_max': price_max, 'night_min': night_min,
            'night_max': night_max, 'tour_end': tour_end}

    return render(request, 'departure.html', {'menu_header': departures, 'departures': tours_dict, 'info': info})


def TourView(request, id):
    """ Тур """
    tour = tours.get(id)
    return render(request, 'tour.html', {'menu_header': departures, 'tour': tour})


def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1>Ошибка 404</h1></p><p><h2>Такой страницы не существует</h2>')


def custom_handler500(request):
    return HttpResponseServerError(
        '<p><h1>Ошибка 500</h1></p><p><h2>Ошибка на сервере</h2></p>')
