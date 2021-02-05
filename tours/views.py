from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.shortcuts import render


def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1>Ошибка 404</h1></p><p><h2>Такой страницы не существует</h2>')


def custom_handler500(request):
    return HttpResponseServerError(
        '<p><h1>Ошибка 500</h1></p><p><h2>Ошибка на сервере</h2></p>')


def MainView(request):
    """ Главная """
    return render(request, 'index.html')


def DepartureView(request):
    """ Направление """
    return render(request, 'departure.html')


def TourView(request):
    """ Тур """
    return render(request, 'tour.html')
