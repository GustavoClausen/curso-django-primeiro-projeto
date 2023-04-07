import os

from django.contrib import messages
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe
from utils.pagination import make_pagination

ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 6))


def root_page(request):

    messages.warning(request, 'Seja bem vindo à página HOME')

    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request=request,
        queryset=recipes,
        items_per_page=ITEMS_PER_PAGE,
    )

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
    })


def recipe(request, id):

    # recipe = Recipe.objects.filter().order_by('-id').first()

    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

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

    page_obj, pagination_range = make_pagination(
        request=request,
        queryset=recipes,
        items_per_page=ITEMS_PER_PAGE,
    )

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'Category - {recipes[0].category.name}',
    })


def search(request):

    search_term = request.GET.get('s', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        # icontains --> ignora letras maísculas ou minúsculas
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True,
    ).order_by('-id')

    # recipes = recipes.order_by('-id')
    # recipes = recipes.filter(is_published=True)

    page_obj, pagination_range = make_pagination(
        request=request,
        queryset=recipes,
        items_per_page=ITEMS_PER_PAGE,
    )

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Pesquisa por "{search_term}"',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&s={search_term}',
    })
