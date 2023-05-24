import os

from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            request=self.request,
            queryset=ctx.get('recipes'),
            items_per_page=ITEMS_PER_PAGE,
        )
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('s', '').strip()

        if not search_term:
            raise Http404()

        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            ),
            is_published=True,
        ).order_by('-id')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('s', '').strip()
        ctx.update(
            {
                'page_title': f'Pesquisa por "{search_term}"',
                'search_term': search_term,
                'additional_url_query': f'&s={search_term}',
            }
        )
        return ctx


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id'),
        )
        return qs


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
