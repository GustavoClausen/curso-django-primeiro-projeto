from django.urls import path
from recipes.views import root_page, about_page, contact_page

urlpatterns = [
    path('', root_page),              # http://127.0.0.1/
    path('sobre/', about_page),         # http://127.0.0.1/sobre/
    path('contato/', contact_page)      # http://127.0.0.1/contato/
]
