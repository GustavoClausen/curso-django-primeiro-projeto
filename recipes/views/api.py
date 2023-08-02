from django.shortcuts import get_object_or_404
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


@api_view(http_method_names=['get'])
def api_recipe_list(request):
    recipes = Recipe.objects.get_published()[:10]
    serializer = RecipeSerializer(
        instance=recipes,
        many=True,
        context={'request': request},
    )
    return Response(serializer.data)


@api_view(http_method_names=['get'])
def api_recipe_detail(request, pk):
    # PARA PERSONALIZAR UM POUCO MAIS A RESPONSE
    # recipe = Recipe.objects.get_published().filter(pk=pk).first()
    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe, many=False)
    #     return Response(serializer.data)
    # else:
    #     return Response(
    #         {
    #             'detail': 'Aqui vai sua mensagem de erro',
    #         },
    #         status=status.HTTP_404_NOT_FOUND,
    #     )
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk,
    )
    serializer = RecipeSerializer(
        instance=recipe,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)


@api_view(http_method_names=['get'])
def api_tag_list(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk,
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
