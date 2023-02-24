from django.urls import path

from . import views

urlpatterns = [
    path('', views.root_page),              # http://127.0.0.1/
    path('recipes/<int:id>/', views.recipe),
]
