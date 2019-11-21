"""Peliculas URL Configuration


"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views import static
from principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'media/(?P<path>.*)', static.serve,
            {'document_root': settings.MEDIA_ROOT,}),
    path('sobre/',views.sobre),
    path('usuarios/', views.usuarios),
    path('recetas/', views.lista_recetas),
    re_path(r'receta/(?P<id_receta>\d+)',views.detalle_receta),
    path('',views.inicio),
    ]
