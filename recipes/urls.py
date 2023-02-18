from django.urls import path

from recipes.views import root_page

urlpatterns = [
    path('', root_page),              # http://127.0.0.1/
]
