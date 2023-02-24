from django.shortcuts import render


def root_page(request):
    return render(request, 'recipes/pages/home.html', {
        'name': 'Gustavo',
        'lastname': 'Clausen'
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html')
