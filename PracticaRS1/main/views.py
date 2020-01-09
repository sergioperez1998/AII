#encoding:utf-8
from django.shortcuts import render
from main.models import Artista

# Create your views here.
path = "C:\\Users\\Usuario\\Desktop\\Universidad\\cuarto año\\AII\\repositorio git\\AII\\PracticaRecomendacion\\data"



def populateArtista():
    print("Cargando artista...")
    
    lista=[]
    fileobj=open(path+"\\artists.txt", "r")
    
 
    i=0
    
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        if len(rip) != 4:
            continue
        if  i!=0:
        
           
            u=Artista(idArtista=rip[0], name=rip[1], url=rip[2], pictureUrl=rip[3])
            lista.append(u) 
        i=i+1   
    fileobj.close()
    Artista.objects.bulk_create(lista)
    
    print("Artistas insertados: " + str(Artista.objects.all().count()))
    print("---------------------------------------------------------")
    
        
if __name__ == '__main__':
    populateArtista()

