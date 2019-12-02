from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('eventos_municipio/',views.mostrar_eventos),
    path('idiomas_eventos/',views.mostrar_eventos_idioma),
    path('eventos_frecuentes/',views.mostrar_mejores_eventos),
    path('busqueda_eventos/',views.mostrar_eventos_fecha),
    path('',views.index),
    path('index.html/', views.index),
    path('populate/', views.populateDatabase),
    path('ingresar/', views.ingresar),    
    path('admin/',admin.site.urls),
    ]
