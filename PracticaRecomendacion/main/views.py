from django.shortcuts import render

# Create your views here.

path = "C:\\Users\\Usuario\\Desktop\\Universidad\\cuarto año\\AII\\Proyecto git\\ProyectoAii\\JSGames\\data"



def populateVideoJuegosNintendoSwitch():
    print("Cargando artista...")
    Artista.objects.all.delete()
    lista=[]
    listaAux=[]
    listaGeneros=[]
    dict_generos={}
    listaIdJuegos=[]
    fileobj=open(path+"\\artists.txt", "r")
    
 
    i=0
    
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        if len(rip) != 4:
            continue
        if  i!=0:
        
           
            u=Artista(id=rip[0], name=rip[1], url==rip[2] ,pictureUrl=rip[3])
            lista.append(u)
        i=i+1   
    fileobj.close()
    Artista.objects.bulk_create(lista)
    dict2={}
   
    for Artista in Artista.Objects.all():
        juegosNintendoSwitch.generos.set(dict_generos[juegosNintendoSwitch.idVideoJuegos])
        dict2[juegosNintendoSwitch.idVideoJuegos]=juegosNintendoSwitch
    
    print("Videojuego insertados: " + str(VideoJuego.objects.filter(consola__nombre="Nintendo Switch").count()))
    print("---------------------------------------------------------")

