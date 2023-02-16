"""projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse


def about_page(request):
    return HttpResponse('Uma string da página <b> SOBRE </b>')


def root_page(request):
    return HttpResponse('Essa é a página <b> ROOT </b>')


def contact_page(request):
    return HttpResponse('Essa é a página de "CONTATO" ')


urlpatterns = [
    path('admin/', admin.site.urls),    # http://127.0.0.1/admin/
    path('', root_page),                # http://127.0.0.1/
    path('sobre/', about_page),         # http://127.0.0.1/sobre/
    path('contato/', contact_page)      # http://127.0.0.1/contato/
]
