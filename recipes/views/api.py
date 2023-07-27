from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(http_method_names=['get'])
def api_recipe_list(request):
    return Response({
        "name": "TESTE",
    })
