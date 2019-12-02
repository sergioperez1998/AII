#encoding:utf-8
from main.models import Usuario, Ocupacion, Puntuacion, Pelicula, Categoria
from main.forms import  UsuarioBusquedaForm, PeliculaBusquedaYearForm
from django.shortcuts import render
from django.db.models import Avg
from django.http.response import HttpResponseRedirect, HttpResponse
from django.conf import settings
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

path = "C:\\Users\\sergi\\Desktop\\Mi Equipo\\Facultad\\CUARTO CURSO\\ACCESO INTELIGENTE A LA INFORMACION\\REPO\\AII\\EjercicioDjango\\data"

#Funcion de acceso restringido que carga los datos en la BD  
@login_required(login_url='/ingresar')
def populateDatabase(request):
    
    populateGenres()
    u=populateUsers()
    m=populateMovies()
    populateRatings(u,m)  #USAMOS LOS DICCIONARIOS DE USUARIOS Y PELICULAS PARA ACELERAR LA CARGA EN PUNTUACIONES
    
    
    populateLenguas()
    populateTipoEvento()
    populateMunicipio()
    logout(request)  # se hace logout para obligar a login cada vez que se vaya a poblar la BD
    return HttpResponseRedirect('/index.html')


def mostrar_ocupaciones(request):
    usuarios= Usuario.objects.all().order_by('ocupacion')
    return render(request, 'ocupacion_usuarios.html',{'usuarios':usuarios, 'STATIC_URL':settings.STATIC_URL})


def mostrar_mejores_peliculas(request):  
    peliculas = Pelicula.objects.annotate(avg_rating=Avg('puntuacion__puntuacion')).order_by('-avg_rating')[:5]
    return render(request, 'mejores_peliculas.html', {'peliculas':peliculas, 'STATIC_URL':settings.STATIC_URL})


def mostrar_peliculas_year(request):
    formulario = PeliculaBusquedaYearForm()
    peliculas = None
    
    if request.method=='POST':
        formulario = PeliculaBusquedaYearForm(request.POST)
        
        if formulario.is_valid():
            peliculas = Pelicula.objects.filter(fechaEstreno__year=formulario.cleaned_data['year'])
            
    return render(request, 'busqueda_peliculas.html', {'formulario':formulario, 'peliculas':peliculas, 'STATIC_URL':settings.STATIC_URL})


def mostrar_puntuaciones_usuario(request):
    formulario = UsuarioBusquedaForm()
    puntuaciones = None
    
    if request.method=='POST':
        formulario = UsuarioBusquedaForm(request.POST)
        
        if formulario.is_valid():
            puntuaciones = Puntuacion.objects.filter(idUsuario = Usuario.objects.get(pk=formulario.cleaned_data['idUsuario']))
            
    return render(request, 'puntuaciones_usuario.html', {'formulario':formulario, 'puntuaciones':puntuaciones, 'STATIC_URL':settings.STATIC_URL})



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
    
    print("Lenguages inserted: " + str(Lenguaje.objects.count()))
    print("---------------------------------------------------------")
    
def populateTipoEvento():
    
    print("Loading languages...")
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
        lista_eventos.append(Evento(nombre=rip[0], tipo=Tipo.objects.get(nombre=rip[1]), fechaInicio=rip[2],fechaFin=rip[3], precio=rip[4],lenguaje=Lenguaje.objects.get(nombre=rip[5],municipio=Municipio.objects.get(nombre=rip[6])))
        idioma = rip[5]
        if "/" in string:
            parseado0 = idioma.strip().split("/")[0]
            parseado1 = idioma.strip().split("/")[1]
            lista_idioma.append(Lenguaje.objects.get(pk =parseado0))
            lista_idioma.append(Lenguaje.objects.get(pk =parseado1))
        else:
            lista_idioma.append(Lenguaje.objects.get(pk =idioma))
    fileobj.close()    
    Pelicula.objects.bulk_create(lista_peliculas)

    dict={}
    for pelicula in Pelicula.objects.all():
        pelicula.categorias.set(dict_categorias[pelicula.idPelicula])
        dict[pelicula.idPelicula]=pelicula
    
    print("Movies inserted: " + str(Pelicula.objects.count()))
    print("---------------------------------------------------------")
    return(dict)













def populateTipoEvento():
    print("Loading type events...")
    Tipo.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\tipoevento.csv", "r")
    i=0
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


    
