from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,HttpResponse
from django.conf import settings
from principal.models import  Usuario,Director,Pelicula

def sobre(request):
    html="<html><body>Proyecto de ejemplo de vistas</body></htm>"
    return HttpResponse(html)

def usuarios(request):
    usuarios=Usuario.objects.all()
    return render(request,'inicio.html', {'usuarios':usuarios})



def lista_peliculas(request):
    peliculas=Pelicula.objects.all()
    return render(peliculas,'peliculas.html', {'peliculas':peliculas})

def lista_directores(request):
    directores=Director.objects.all()
    return render(directores,'directores.html', {'directores':directores})



# Create your views here.
