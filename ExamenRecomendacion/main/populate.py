#encoding:utf-8
import csv
from datetime import datetime
from main.models import Libro, Usuario, Puntuacion
path = "C:\\Users\\Usuario\\Desktop\\archivos\\data"

def populateLibro():
    print("Cargando Libros...")
    Libro.objects.all().delete()
    lista=[]
    listaDePuntaciones=[]
    archivo = open(path+"\\bookfeatures.csv",encoding="utf-8")
    reader = csv.reader(archivo,delimiter=';')
    i=0
    for line in reader:
        if len(line) != 10:
            continue
        
        if  i!=0:
            print(line)
                
        
            listaDePuntaciones.append(line[5])
            listaDePuntaciones.append(line[6])
            listaDePuntaciones.append(line[7])
            listaDePuntaciones.append(line[8])
            listaDePuntaciones.append(line[9])
                
            u=Libro(bookId=line[0], titulo=line[1], autor=line[2], genero=line[3], idioma=line[4], puntuaciones=listaDePuntaciones)
            lista.append(u) 
            
        i=i+1   
    
    Libro.objects.bulk_create(lista)
    
    print("Libros insertados: " + str(Libro.objects.all().count()))
    print("---------------------------------------------------------")

def populateUsuario():
    print("Cargando usuarios...")
    Usuario.objects.all().delete()
    lista=[]
    archivo = open(path+"\\ratings.csv",encoding="utf-8")
    reader = csv.reader(archivo,delimiter=';')
    
    i=0
    
    for line in reader:
        if  len(line)!=3:
            continue
            if  i!=0:
        
        
           
                u=Usuario(idUsuario=line[1])
                if u not in lista:
                    lista.append(u) 
            
        i=i+1   
    
    Usuario.objects.bulk_create(lista)
    
    print("Usuarios insertadas: " + str(Usuario.objects.all().count()))
    print("---------------------------------------------------------")
    
def populatePuntuaciones():
    print("Cargando Puntuaciones...")
    Puntuacion.objects.all().delete()
    lista=[]
    archivo = open(path+"\\ratings.csv",encoding="utf-8")
    reader = csv.reader(archivo,delimiter=';')
    i=0
    for line in reader:
        
        if  len(line)!=10:
            continue
            if  i!=0:
        
                
                u=Puntuacion(bookId=line[0], idUsuario=Usuario.objects.get(idUsuario=line[1]), puntuacion=line[2])
                lista.append(u) 
                
                print(lista)
        i=i+1   
    
    Puntuacion.objects.bulk_create(lista)
    print(lista)
    
    print("Puntuaciones insertadas: " + str(Puntuacion.objects.all().count()))
    print("---------------------------------------------------------")




def populateDatabase():
    populateLibro()
    populateUsuario()
    populatePuntuaciones()
    print("Base de datos populada")
    
    
if __name__ == '__main__':
    populateDatabase()