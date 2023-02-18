from django.shortcuts import render


def root_page(request):
    return render(request, 'recipes/home.html', {
        'name': 'Gustavo',
        'lastname': 'Clausen'
    })
