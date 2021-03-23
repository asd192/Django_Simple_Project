import random

from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

import tours.data as tours_data


def main_view(request):
    """ Главная """

    # перемешиваем доступные ключи словарей
    tours_random = list(tours_data.tours.keys())
    random.shuffle(tours_random)

    # формируем список словарей
    tours_dict = dict()
    for number in tours_random[:6]:
        tours_dict[number] = tours_data.tours[number]

    about = {
        'title': tours_data.title,
        'subtitle': tours_data.subtitle,
        'description': tours_data.description
    }

    context = {
        'menu_header': tours_data.departures,
        'about': about,
        'tours': tours_dict
    }

    return render(request, 'tours/index.html', context=context)


def departure_view(request, departure):
    """ Направления """
    if departure not in tours_data.departures.keys():
        raise Http404

    tours_dict, price, night = dict(), [], []
    for num, tour in tours_data.tours.items():
        if tours_data.tours[num]['departure'] == departure:
            tours_dict[num] = tour

            # прайс и ночи, от и до
            price.append(int(tour['price']))
            night.append(int(tour['nights']))

    tours_count = len(tours_dict)

    # информация о найденых турах
    fly_from = tours_data.departures[departure]

    info = {
        'tours_count': tours_count,
        'price_min': min(price),
        'price_max': max(price),
        'night_min': min(night),
        'night_max': max(night)
    }

    context = {
        'menu_header': tours_data.departures,
        'departures': tours_dict,
        'info': info,
        'fly_from': fly_from
    }

    return render(request, 'tours/departure.html', context=context)


def tour_view(request, id_tour):
    """ Тур """
    tour = tours_data.tours.get(id_tour, False) or False

    if not tour:
        raise Http404

    tour_to_where = tours_data.departures[tour['departure']]

    context = {
        'menu_header': tours_data.departures,
        'tour': tour,
        'tour_to_where': tour_to_where
    }

    return render(request, 'tours/tour.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound(render(request, '404.html'))


def custom_handler500(request):
    return HttpResponseServerError(render(request, '500.html'))
