import random

from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError

from tours.data import tours


def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1>Ошибка 404</h1></p><p><h2>Такой страницы не существует</h2>')


def custom_handler500(request):
    return HttpResponseServerError(
        '<p><h1>Ошибка 500</h1></p><p><h2>Ошибка на сервере</h2></p>')


def MainView(request):
    """ Главная """

    # Туры
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

    return render(request, 'index.html', {'tours': tours_dict})


def DepartureView(request, departure):
    """ Направление """
    return render(request, 'departure.html', tours)


def TourView(request, id):
    """ Тур """
    tour = tours.get(id)
    return render(request, 'tour.html', tour)
