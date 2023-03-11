from django.shortcuts import get_list_or_404, render

from recipes.models import Recipe

# from utils.recipes.factory import make_recipe


def root_page(request):

    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def recipe(request, id):

    recipe = Recipe.objects.filter(
        pk=id,
        is_published=True
    ).order_by('-id').first()

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def category(request, category_id):

    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True
        ).order_by('-id'))

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'Category - {recipes[0].category.name}'
    })
