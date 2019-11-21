from principal.models import Receta, Comentario
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,HttpResponse
from django.conf import settings

def sobre(request):
    html="<html><body>Proyecto de ejemplo de vistas</body></htm>"
    return HttpResponse(html)

def inicio(request):
    recetas=Receta.objects.all()
    return render(request,'inicio.html', {'recetas':recetas})

def usuarios(request):
    recetas=Receta.objects.all()
    usuarios=User.objects.all()
    return render(request,'usuarios.html', {'recetas':recetas,'usuarios':usuarios})

def lista_recetas(request):
    recetas=Receta.objects.all()
    return render(request,'recetas.html', {'datos':recetas,'MEDIA_URL': settings.MEDIA_URL})

def detalle_receta(request, id_receta):
    dato = get_object_or_404(Receta, pk=id_receta)
    comentarios=Comentario.objects.filter(receta=id_receta)
    return render(request,'receta.html',{'receta':dato, 'comentarios':comentarios,'MEDIA_URL': settings.MEDIA_URL})