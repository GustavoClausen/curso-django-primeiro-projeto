from django.http import HttpResponse


def root_page(request):
    return HttpResponse('Essa é a página <b> ROOT 2</b>')


def about_page(request):
    return HttpResponse('Uma string da página <b> SOBRE 2</b>')


def contact_page(request):
    return HttpResponse('Essa é a página de <b> CONTATO 2</b>')
