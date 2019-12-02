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

path = "C:\\Users\\Usuario\\Desktop\\Universidad\\cuarto año\\AII\\repositorio git\\AII\\EjercicioDjango\\data"

#Funcion de acceso restringido que carga los datos en la BD  
@login_required(login_url='/ingresar')
def populateDatabase(request):
    populateOccupations()
    populateGenres()
    u=populateUsers()
    m=populateMovies()
    populateRatings(u,m)  #USAMOS LOS DICCIONARIOS DE USUARIOS Y PELICULAS PARA ACELERAR LA CARGA EN PUNTUACIONES
    logout(request)  # se hace logout para obligar a login cada vez que se vaya a poblar la BD
    return HttpResponseRedirect('/index.html')


def mostrar_eventos(request):
    eventos= Evento.objects.all().order_by('municipio')
    return render(request, 'eventos_municipio.html',{'eventos':eventos, 'STATIC_URL':settings.STATIC_URL})


def mostrar_mejores_eventos(request):  
    eventos = Evento.objects.annotate(numeroTipo=Count('tipo')).order_by('-numeroTipo')[:2]
    return render(request, 'eventos_frecuenes.html', {'eventos':eventos, 'STATIC_URL':settings.STATIC_URL})
    


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


def populateOccupations():
    print("Loading occupations...")
    Ocupacion.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\u.occupation", "r")
    for line in fileobj.readlines():
        lista.append(Ocupacion(nombre=str(line.strip())))
    fileobj.close()
    Ocupacion.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    print("Occupations inserted: " + str(Ocupacion.objects.count()))
    print("---------------------------------------------------------")


def populateGenres():
    print("Loading Movie Genres...")
    Categoria.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\u.genre", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 2:
            continue
        lista.append(Categoria(idCategoria=rip[1], nombre=rip[0]))
    fileobj.close()
    Categoria.objects.bulk_create(lista)
    
    print("Genres inserted: " + str(Categoria.objects.count()))
    print("---------------------------------------------------------")


def populateUsers():
    print("Loading users...")
    Usuario.objects.all().delete()
    
    lista=[]
    dict={}
    fileobj=open(path+"\\u.user", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 5:
            continue
        u=Usuario(idUsuario=rip[0], edad=rip[1], sexo=rip[2], ocupacion=Ocupacion.objects.get(nombre=rip[3]), codigoPostal=rip[4])
        lista.append(u)
        dict[rip[0]]=u
    fileobj.close()
    Usuario.objects.bulk_create(lista)
    
    print("Users inserted: " + str(Usuario.objects.count()))
    print("---------------------------------------------------------")
    return(dict)

def populateMovies():
    print("Loading movies...")
    Pelicula.objects.all().delete()
    
    lista_peliculas =[]  # lista de peliculas
    dict_categorias={}  #  diccionario de categorias de cada pelicula (idPelicula y lista de categorias)
    fileobj=open(path+"\\u.item", "r")
    for line in fileobj.readlines():
        rip = line.strip().split('|')
        
        date = None if len(rip[2]) == 0 else datetime.strptime(rip[2], '%d-%b-%Y')
        lista_peliculas.append(Pelicula(idPelicula=rip[0], titulo=rip[1], fechaEstreno=date, imdbUrl=rip[4]))
        
        lista_aux=[]
        for i in range(5, len(rip)):
            if rip [i] == '1':
                lista_aux.append(Categoria.objects.get(pk = (i-5)))
        dict_categorias[rip[0]]=lista_aux
    fileobj.close()    
    Pelicula.objects.bulk_create(lista_peliculas)

    dict={}
    for pelicula in Pelicula.objects.all():
        pelicula.categorias.set(dict_categorias[pelicula.idPelicula])
        dict[pelicula.idPelicula]=pelicula
    
    print("Movies inserted: " + str(Pelicula.objects.count()))
    print("---------------------------------------------------------")
    return(dict)

def populateRatings(u,m):
    print("Loading ratings...")
    Puntuacion.objects.all().delete()

    lista=[]
    fileobj=open(path+"\\u.data", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        lista.append(Puntuacion(idUsuario=u[rip[0]], idPelicula=m[rip[1]], puntuacion=rip[2]))
    fileobj.close()
    Puntuacion.objects.bulk_create(lista)
    print("Ratings inserted: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")


    
