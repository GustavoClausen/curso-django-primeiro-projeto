from django.http import HttpResponse
from django.shortcuts import render


def root_page(request):
    return render(request, 'recipes/home.html', {
        'name': 'Gustavo',
        'lastname': 'Clausen'
    })


def about_page(request):
    return HttpResponse('Uma string da página <b> SOBRE 2</b>')


def contact_page(request):
    return render(request, 'temp/temp.html')
