encoding = "utf-8"
from bs4 import BeautifulSoup
import urllib.request as urllib2
import datetime
from tkinter import *
from tkinter import messagebox
import os
from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser

def llamadaObtencionDatos():
    
    i=1
    lista=[]
    
    while i<4:
        url="http://www.sensacine.com/noticias/?page="+str(i)
        if i == 1:
            lista=obtenerDatos(url)
        else:
            lista[0].extend(obtenerDatos(url)[0])
            lista[1].extend(obtenerDatos(url)[1])
            lista[2].extend(obtenerDatos(url)[2])
            lista[3].extend(obtenerDatos(url)[3])
            lista[4].extend(obtenerDatos(url)[4])
        i=i+1
     
    return lista

def obtenerDatos(url):
    
    urlBasica="http://www.sensacine.com/"
    response = urllib2.urlopen(url)
    webContent = response.read()
    soup = BeautifulSoup(webContent, 'html.parser')
    
    listaCategoria=[]
    listaTitulos=[]
    listaEnlaces=[]
    listaFechas=[]
    listaDescripciones=[]
    meses={"enero":"01", "febrero":"02", "marzo":"03", "abril":"04", "mayo":"05", "junio":"06", "julio":"07", "agosto":"08", "septiembre":"09", "octubre":"10", "noviembre":"11", "diciembre":"12" }
    
    for categorias in soup.findAll("div",attrs={"class":"meta-category"}):
        listaCategoria.append(categorias.string.split("-")[1].strip(" "))
    for titulos in soup.findAll("a",attrs={"class":"meta-title-link"}):
        listaTitulos.append(titulos.string.strip())
        listaEnlaces.append(urlBasica+titulos.get("href"))
    for fechas in soup.findAll("div",attrs={"class":"meta-date"}):
        fechaSinCasting=fechas.string.split(" ")[1]+ "/" + meses[fechas.string.split(" ")[3]] + "/" + fechas.string.split(" ")[5]
        fechasCasting= datetime.datetime.strptime(fechaSinCasting, '%d/%m/%Y')
        listaFechas.append(fechasCasting)
    for descripciones in soup.findAll("div",attrs={"class":"meta-body"}):
        listaDescripciones.append(descripciones.string)
        
    return listaCategoria, listaTitulos, listaEnlaces, listaFechas ,listaDescripciones
        
def apartado_a(dirdocs,dirindex):
    if not os.path.exists(dirdocs):
        print ("Error: no existe el directorio de documentos " + dirdocs)
    else:
        if not os.path.exists(dirindex):
            os.mkdir(dirindex)

    ix = create_in(dirindex, schema=get_schema())
    writer = ix.writer()
    i=0
    for docname in os.listdir(dirdocs):
        if not os.path.isdir(dirdocs+docname):
            add_doc(writer, dirdocs, docname)
            i+=1
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " correos")
            
    writer.commit() 

  
def apartado_b(dirindex):
    query = input("Introduzca palabras titulo o descripcion: ")
    ix=open_dir(dirindex)   

    with ix.searcher() as searcher:
        query = QueryParser("titulo", ix.schema,group=qparser.OrGroup).parse(query)
        results = searcher.search(query)
        for r in results:
            print ("FICHERO: "+r['nombrefichero'])
          
def get_schema():
    return Schema(titulo=TEXT(stored=True), categoria=TEXT(stored=True), enlace=TEXT(stored=True),fecha=DATETIME(stored=True), descripcion=TEXT(stored=True),nombrefichero=ID(stored=True) )


def add_doc(writer, path, docname):
    try:    
        fileobj=open(path+'\\'+docname, "r")
        tit=fileobj.readline().strip()
        cate=fileobj.readline().strip()
        enl=fileobj.readline().strip()
        f=fileobj.readline().strip()
        fe=datetime.strptime(f,'%Y%m%d')
        descrip=fileobj.read()
        fileobj.close()           
        
        writer.add_document(titulo=tit, categoria=cate, enlace=enl, fecha=fe, descripcion=descrip,nombrefichero=docname)
          
        print("Creado indice para fichero " + docname)
    except:
        print ("Error: No se ha podido añadir el documento "+path+'\\'+docname)
        
        
    
def ventana_principal():
    dirdocs="txts"
    dirindex="Index"
    top = Tk()
    indexar = Button(top, text="Indexar", command = lambda: apartado_a(dirdocs,dirindex))
    indexar.pack(side = TOP)
    Buscar = Button(top, text="Buscar por Rtte", command = lambda: apartado_b(dirindex))
    Buscar.pack(side = TOP)
    top.mainloop()


if __name__ == '__main__':
    ventana_principal() 