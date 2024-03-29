import os

from django.db.models import F, Q, Value
from django.db.models.aggregates import Count
from django.db.models.functions import Concat
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView

from recipes.models import Recipe
from tag.models import Tag
from utils.pagination import make_pagination

ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 6))


def theory(request, *args, **kwargs):
    # A query só será executada se for utilizado um valor dela
    # recipes = Recipe.objects.all()
    # recipes = recipes.filter(title__icontains='Teste')

    # recipes = Recipe.objects.values('id', 'title') \
    #     .filter(title__icontains='Vegano')
    # number_of_recipes = recipes.aggregate(number=Count('id'))

    recipes = Recipe.objects.all().annotate(
        author_full_name=Concat(
            F('author__username'),
            Value(' ('),
            F('author__first_name'),
            Value(' '),
            F('author__last_name'),
            Value(')'),
        )
    )

    number_of_recipes = recipes.aggregate(number=Count('id'))

    context = {
        'recipes': recipes,
        'number_of_recipes': number_of_recipes['number'],
    }

    return render(
        request,
        'recipes/pages/theory.html',
        context=context,
    )


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            request=self.request,
            queryset=ctx.get('recipes'),
            items_per_page=ITEMS_PER_PAGE,
        )
        html_language = translation.get_language()
        ctx.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range,
                'html_language': html_language,
            }
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeAPI(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):

        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False,
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id'),
        )

        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        category_translation = _('Category')
        ctx.update(
            {
                'title': f'{category_translation} - {ctx.get("recipes")[0].category.name}',  # noqa
            }
        )
        return ctx


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


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(is_published=True)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True,
        })
        return ctx


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri()[:21] + \
                recipe_dict['cover'].url
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects \
            .filter(slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = page_title
        ctx.update(
            {
                'page_title': page_title,
            }
        )
        return ctx
