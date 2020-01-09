#encoding:utf-8
from django.shortcuts import render
from main.models import Artista, Etiqueta, Usuario, UsuarioArtista,\
    UsuarioEtiquetaArtista
from django.conf import settings
from datetime import datetime

# Create your views here.

path = "C:\\Users\\Usuario\\Desktop\\Universidad\\cuarto año\\AII\\repositorio git\\AII\\PracticaRecomendacion\\data"

def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})


def populateArtista():
    print("Cargando artista...")
    Artista.objects.all().delete()
    lista=[]
    fileobj=open(path+"\\artists.dat", "r",encoding="utf-8")
    
 
    i=0
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        print(len(rip))
        if  len(rip)==4:
            if  i!=0:
        
          
                u=Artista(idArtista=rip[0], name=rip[1], url=rip[2], pictureUrl=rip[3])
                lista.append(u) 
        elif len(rip)==3:
            if  i!=0:
                u=Artista(idArtista=rip[0], name=rip[1], url=rip[2])
                lista.append(u) 
            
        i=i+1   
    fileobj.close()
    Artista.objects.bulk_create(lista)
    
    print("Artistas insertados: " + str(Artista.objects.all().count()))
    print("---------------------------------------------------------")
    print(Artista.objects.all())

def populateEtiqueta():
    print("Cargando etiquetas...")
    Etiqueta.objects.all().delete()
    lista=[]
  
    fileobj=open(path+"\\tags.dat", "r",encoding="latin-1")
    
    i=0
    
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        if len(rip) != 2:
            continue
        if  i!=0:
        
           
            u=Etiqueta(id=rip[0], tagValue=rip[1],)
            lista.append(u) 
        i=i+1   
    fileobj.close()
    Etiqueta.objects.bulk_create(lista)
    
    print("Etiquetas insertadas: " + str(Etiqueta.objects.all().count()))
    print("---------------------------------------------------------")

def populateUsuario():
    print("Cargando usuarios...")
    Usuario.objects.all().delete()
    lista=[]
    fileobj=open(path+"\\user_friends.dat", "r")
    
    i=0
    
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        if len(rip) != 2:
            continue
        if  i!=0:
        
           
            u=Usuario(idUsuario=rip[0])
            if u not in lista:
                lista.append(u) 
            
        i=i+1   
    fileobj.close()
    Usuario.objects.bulk_create(lista)
    
    print("Usuarios insertadas: " + str(Usuario.objects.all().count()))
    print("---------------------------------------------------------")
    
def populateUsuarioArtista():
    print("Cargando usuariosArtistas...")
    UsuarioArtista.objects.all().delete()
    lista=[]
    fileobj=open(path+"\\user_artists.dat", "r")
    
    i=0
    
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        if len(rip) != 3:
            continue
        if  i!=0:
        
            
            u=UsuarioArtista(idUsuario=Usuario.objects.get(idUsuario=rip[0]), idArtista=Artista.objects.get(idArtista=rip[1]),tiempoEscucha=rip[2]) 
            lista.append(u)
        i=i+1   
    fileobj.close()
    UsuarioArtista.objects.bulk_create(lista)
    
    print("UsuariosArtistas insertadas: " + str(UsuarioArtista.objects.all().count()))
    print("---------------------------------------------------------")

def populateUsuarioEtiquetaArtista():
    print("Cargando usuariosEtiquetaArtistas...")
    UsuarioEtiquetaArtista.objects.all().delete()
    lista=[]
    fileobj=open(path+"\\user_taggedartists.dat", "r")
    
    i=0
    
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        if len(rip) != 6:
            continue
        if  i!=0:
            try:
                u=UsuarioEtiquetaArtista(idUsuario=Usuario.objects.get(idUsuario=rip[0]), idArtista=Artista.objects.get(idArtista=rip[1]),idTag=Etiqueta.objects.get(id=rip[2]),fecha=datetime.strptime(rip[3]+"-"+rip[4]+"-"+rip[5],'%d-%m-%Y')) 
                lista.append(u)
            except Artista.DoesNotExist:
                break
            
        i=i+1   
    fileobj.close()
    UsuarioEtiquetaArtista.objects.bulk_create(lista)
    
    print("UsuarioEtiquetaArtista insertadas: " + str(UsuarioEtiquetaArtista.objects.all().count()))
    print("---------------------------------------------------------")



#populateArtista()
#populateEtiqueta()
#populateUsuario()
#populateUsuarioArtista()
#populateUsuarioEtiquetaArtista()



