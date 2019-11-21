from datetime import datetime as datetime2
from bs4 import BeautifulSoup
import urllib.request
import datetime
from tkinter import *
from tkinter import messagebox
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
import os, os.path
from whoosh import index,fields
from unicodedata import normalize
import errno
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser
from whoosh.qparser.dateparse import DateParserPlugin

def eliminadorDiacriticos(cadena):
    
    s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
    normalize("NFD", cadena), 0, re.I)
    s = normalize('NFC', s)
    return s


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
    response = urllib.request.urlopen(url)
    
    soup = BeautifulSoup(response.read().decode("latin-1"), 'html.parser')
    
    listaCategoria=[]
    listaTitulos=[]
    listaEnlaces=[]
    listaFechas=[]
    listaDescripciones=[]
    meses={"enero":"01", "febrero":"02", "marzo":"03", "abril":"04", "mayo":"05", "junio":"06", "julio":"07", "agosto":"08", "septiembre":"09", "octubre":"10", "noviembre":"11", "diciembre":"12" }
    
    for categorias in soup.findAll("div",attrs={"class":"meta-category"}):
        listaCategoria.append(categorias.string.split("-")[1].strip(" "))
        for titulos in soup.findAll("a",attrs={"class":"meta-title-link"}):
            TituloSinParsear=titulos.string.strip()
            TituloParseado = eliminadorDiacriticos(TituloSinParsear)
            listaTitulos.append(TituloParseado)
            listaEnlaces.append(urlBasica+titulos.get("href"))
        for fechas in soup.findAll("div",attrs={"class":"meta-date"}):
            fechaSinCasting=fechas.string.split(" ")[1]+ "/" + meses[fechas.string.split(" ")[3]] + "/" + fechas.string.split(" ")[5]
            fechasCasting= datetime.datetime.strptime(fechaSinCasting, '%d/%m/%Y')
            listaFechas.append(fechasCasting)
        for descripciones in soup.findAll("div",attrs={"class":"meta-body"}):

            listaDescripciones.append(descripciones.string)
    
   
        
    return listaCategoria, listaTitulos, listaEnlaces, listaFechas ,listaDescripciones



def crearTxt():
    

    lista = llamadaObtencionDatos()
    
    try:
        os.mkdir('Documentos')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    for i in range(0,len(lista[0])):


        file_object = open("Documentos\\Archivo"+str(i+1)+".txt","w",encoding='utf-8')
        file_object.write(str(lista[0][i]))
        file_object.write("\n")
        file_object.write(str(lista[1][i]))
        file_object.write("\n")
        file_object.write(str(lista[2][i]))
        file_object.write("\n")
        file_object.write(str(lista[3][i]))
        file_object.write("\n")
        a = lista[4][i]
        b = str(a)
        file_object.write(b)





        
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


            
            
def apartado_b_a(dirindex):
    def mostrar_lista(event):
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            query = QueryParser("titulo", ix.schema ).parse(str(en.get())) | QueryParser("descripcion", ix.schema ).parse(str(en.get()))
            results = searcher.search(query)
            imprimir_b_a(results)
    
    v = Toplevel()
    v.title("Busqueda por titulo  y descripcion")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una o varias palabras  :")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
      

def imprimir_b_a(results):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for r in results:
        lb.insert(END,r['categoria'])
        lb.insert(END,r['titulo'])
        lb.insert(END,r['fecha'])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)  


def apartado_b_b(dirindex):
    def buscarNoticiasFecha(event):
        
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            try:
                fecha = str(en.get())
                fecha1 = fecha.split("-")[0]
                fecha1Consulta = fecha1.split("/")[2]+fecha1.split("/")[1]+fecha1.split("/")[0] 
                fecha2 = fecha.split("-")[1]
                fecha2Consulta = fecha2.split("/")[2]+fecha2.split("/")[1]+fecha2.split("/")[0] 
                myquery='['+ fecha1Consulta + ' to ' +fecha2Consulta+']'
                print(myquery)
                query = QueryParser("fecha", ix.schema).parse(myquery)
           
                results = searcher.search(query)
                imprimir_b_b(results)
            except:
                print ("Error: Formato de fecha incorrecto")
                
    
    v = Toplevel()
    v.title("Busqueda rango de fechas ")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca rango de fechas (DD/MM/AAAA-DD/MM/AAAA):")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", buscarNoticiasFecha)
    en.pack(side=LEFT)
    
  
def imprimir_b_b(results):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for r in results:
        lb.insert(END,r['titulo'])
        lb.insert(END,r['fecha'])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)  
    
def apartado_b_c(dirindex):
    def mostrar_lista(event):
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            query = QueryParser("descripcion", ix.schema ).parse(str(en.get())) 
            results = searcher.search(query)
            imprimir_b_c(results)


    v = Toplevel()
    v.title("Busqueda por descripcion")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una frase :")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
      
def imprimir_b_c(results):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for r in results:
        lb.insert(END,r['titulo'])
        lb.insert(END,r['enlace'])
        lb.insert(END,r['descripcion'])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)  
    
   
   
          
def get_schema():
    return Schema(categoria=TEXT(stored=True), titulo=TEXT(stored=True), enlace=TEXT(stored=True),fecha=DATETIME(stored=True), descripcion=TEXT(stored=True),nombrefichero=ID(stored=True) )


def add_doc(writer, path, docname):
    try:    
        fileobj=open(path+'\\'+docname, "r")
        cate=fileobj.readline().strip()
        tit=fileobj.readline().strip()
        enl=fileobj.readline().strip()
        f=fileobj.readline().strip()
        fe=datetime2.strptime(f,'%Y-%m-%d %H:%M:%S')
        descrip=fileobj.read()
        fileobj.close()           
      
        if descrip==None:
            writer.add_document(categoria=cate,titulo=tit, enlace=enl, descripcion=descrip, nombrefichero=docname)
        else:
            writer.add_document(categoria=cate,titulo=tit, enlace=enl, fecha=fe, descripcion=descrip, nombrefichero=docname)
            
            
        writer.add_document(categoria=cate,titulo=tit, enlace=enl, fecha=fe, descripcion=descrip, nombrefichero=docname)
          
        print("Creado indice para fichero " + docname)
    except:
        
        print("Error: No se ha podido anadir el documento "+path+'\\'+docname)
        
          
        
        
    
def ventanaDatos():
    dirdocs="Documentos\\"
    dirindex="Index"
    top = Tk()
    indexar = Button(top, text="Cargar", command = lambda: apartado_a(dirdocs,dirindex))
    indexar.pack(side = TOP)
    salir = Button(top, text= "Salir", command = quit)
    salir.pack(side = RIGHT)
    top.mainloop()

def ventanaBuscar():
    top = Tk()
    dirindex="Index"

    Buscar = Button(top, text="Buscar por titulo ", command = lambda: apartado_b_a(dirindex))
    Buscar.pack(side = TOP)

    fecha = Button(top, text="Fecha", command = lambda: apartado_b_b(dirindex))
    fecha.pack(side = LEFT)
    Buscar = Button(top, text="Buscar por descripcion ", command = lambda: apartado_b_c(dirindex))
    Buscar.pack(side = TOP)


    top.mainloop()
   

    
def ventanaPrincipal():
    top = Tk()

    almacenarDatos = Button(top, text="Datos", command = ventanaDatos)
    almacenarDatos.pack(side = LEFT)

    buscarOfertas = Button(top, text="Buscar", command = ventanaBuscar)
    buscarOfertas.pack(side = RIGHT)

    top.mainloop()


     



if __name__ == '__main__':
    ventanaPrincipal()
