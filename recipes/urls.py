from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path(
        '',
        views.RecipeListViewHome.as_view(),
        name='home',
    ),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name='search',
    ),
    path(
        'recipes/tags/<slug:slug>',
        views.RecipeListViewTag.as_view(),
        name='tag',
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetail.as_view(),
        name='recipe',
    ),
    path(
        'recipes/api/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name='recipe_detail_api',
    ),
    path(
        'recipes/api/',
        views.RecipeListViewHomeAPI.as_view(),
        name='recipes_api',
    ),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(),
        name='category',
    ),
    path(
        'recipes/theory/',
        views.theory,
        name='theory',
    ),
    path(
        'recipes/api/v2/',
        views.api_recipe_list,
        name='recipe_api_v20',
    ),
    path(
        'recipes/api/v2/<int:pk>/',
        views.api_recipe_detail,
        name='recipe_api_v20_detail',
    ),
    path(
        'recipes/api/v2/tag/<int:pk>/',
        views.api_tag_list,
        name='recipe_api_v20_tag',
    ),
]
