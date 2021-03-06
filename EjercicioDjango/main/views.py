#encoding:utf-8
from main.models import Evento, Tipo, Lenguaje, Municipio
from main.forms import  EventosBusquedaFechaForm, EventosBusquedaIdiomasForm
from django.shortcuts import render
from django.db.models import Avg,Count
from django.http.response import HttpResponseRedirect, HttpResponse
from django.conf import settings
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

<<<<<<< HEAD
path = "C:\\Users\\sergi\\Desktop\\Mi Equipo\\Facultad\\CUARTO CURSO\\ACCESO INTELIGENTE A LA INFORMACION\\REPO\\AII\\EjercicioDjango\\data"
=======
path = "data"
>>>>>>> cf0e707e58c23ff049d73c873c00a57aee74f07f

#Funcion de acceso restringido que carga los datos en la BD  
@login_required(login_url='/ingresar')
def populateDatabase(request):

    populateLenguas()
    populateTipoEvento()
    populateMunicipio()
    populateEventos()
    logout(request)  # se hace logout para obligar a login cada vez que se vaya a poblar la BD
    return HttpResponseRedirect('/index.html')


def mostrar_eventos(request):
    eventos= Evento.objects.all().order_by('municipio')
    return render(request, 'eventos_municipio.html',{'eventos':eventos, 'STATIC_URL':settings.STATIC_URL})


def mostrar_mejores_eventos(request):  
    eventos = Evento.objects.annotate(numeroTipo=Count('tipo')).order_by('-numeroTipo')[:2]
    return render(request, 'eventos_frecuentes.html', {'eventos':eventos, 'STATIC_URL':settings.STATIC_URL})
    


def mostrar_eventos_fecha(request):
    formulario = EventosBusquedaFechaForm()
    eventos = None
    
    if request.method=='POST':
        formulario = EventosBusquedaFechaForm(request.POST)
        
        if formulario.is_valid():
            eventos = Evento.objects.filter(fechaInicio=formulario.cleaned_data['fecha'])
            
    return render(request, 'busqueda_eventos.html', {'formulario':formulario, 'eventos':eventos, 'STATIC_URL':settings.STATIC_URL})


def mostrar_eventos_idioma(request):
    formulario = EventosBusquedaIdiomasForm()
    eventos = None
    
    if request.method=='POST':
        formulario = EventosBusquedaIdiomasForm(request.POST)
        
        if formulario.is_valid():
            eventos = Evento.objects.filter(nombre = Lenguaje.objects.get(full_nombre__startswith=formulario.cleaned_data['nombre']))
            
    return render(request, 'idiomas_eventos.html', {'formulario':formulario, 'eventos':eventos, 'STATIC_URL':settings.STATIC_URL})



def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})

def ingresar(request):
    if request.user.is_authenticated:
        return(HttpResponseRedirect('/populate'))
    formulario = AuthenticationForm()
    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        usuario=request.POST['username']
        clave=request.POST['password']
        acceso=authenticate(username=usuario,password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/populate'))
            else:
                return (HttpResponse('<html><body>ERROR: USUARIO NO ACTIVO </body></html>'))
        else:
            return (HttpResponse('<html><body>ERROR: USUARIO O CONTARSE&Ntilde;A INCORRECTOS </body></html>'))
                     
    return render(request, 'ingresar.html', {'formulario':formulario})
def populateLenguas():
    
    print("Loading languages...")
    Lenguaje.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\lenguas.csv", "r")
    for line in fileobj.readlines():
        lista.append(Lenguaje(nombre=str(line.strip())))
    fileobj.close()
    Lenguaje.objects.bulk_create(lista)
    
    print("Languages inserted: " + str(Lenguaje.objects.count()))
    print("---------------------------------------------------------")
    
def populateTipoEvento():
    
    print("Loading types...")
    Tipo.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\tipoevento.csv", "r")
    for line in fileobj.readlines():
        lista.append(Tipo(nombre=str(line.strip())))
    fileobj.close()
    Tipo.objects.bulk_create(lista)
    
    print("Events type inserted: " + str(Tipo.objects.count()))
    print("---------------------------------------------------------")
    
def populateMunicipio():
    
    print("Loading towns...")
    Municipio.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\municipio.csv", "r")
    for line in fileobj.readlines():
        lista.append(Municipio(nombre=str(line.strip())))
    fileobj.close()
    Municipio.objects.bulk_create(lista)
    
    print("Towns inserted: " + str(Municipio.objects.count()))
    print("---------------------------------------------------------")    

def populateEventos():
    print("Loading events...")
    Evento.objects.all().delete()
    lista_eventos =[]
    lista_idioma=[]
    dict_categorias={}  #  diccionario de categorias de cada pelicula (idPelicula y lista de categorias)
    fileobj=open(path+"\\dataset-B.csv", "r")
    for line in fileobj.readlines():
        rip = line.strip().split(';')
        lista_eventos.append(Evento(nombre=rip[0], tipo=Tipo.objects.get(nombre=rip[1]), fechaInicio=rip[2],fechaFin=rip[3], precio=str(rip[4]),municipio=Municipio.objects.get(nombre=rip[6])))
        idioma = rip[5]
        if "/" in idioma:
            parseado0 = idioma.strip().split("/")[0]
            parseado1 = idioma.strip().split("/")[1]
            lista_idioma.append(Lenguaje.objects.get(pk =parseado0))
            lista_idioma.append(Lenguaje.objects.get(pk =parseado1))
        else:
            lista_idioma.append(Lenguaje.objects.get(pk =idioma))
    fileobj.close()    
    Evento.objects.bulk_create(lista_eventos) 
    
    i=0
    for Eventos in Evento.objects.all():
        Eventos.lenguaje.set(lista_idioma[i])  
        i=i+1 
    print("Events inserted: " + str(Evento.objects.count()))
    print("---------------------------------------------------------")