encoding = "utf-8"
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
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
import os, os.path
from whoosh import index,fields
import errno
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser
from whoosh.qparser.dateparse import DateParserPlugin
from tkinter import *
from tkinter import messagebox
from datetime import datetime as datetime2

def eliminadorDiacriticos(cadena):
    
    s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
    normalize("NFD", cadena), 0, re.I)
    s = normalize('NFC', s)
    return s


def llamadaObtencionDatos():
    
    i=0
    lista=[]
    pagina=9
    
    while i<2:
        url="https://www.sevilla.org/actualidad/noticias?b_start:int=" + str(i*pagina)
        if i == 0:
            lista=obtenerDatos(url)
        else:
            lista[0].extend(obtenerDatos(url)[0])
            lista[1].extend(obtenerDatos(url)[1])
            lista[2].extend(obtenerDatos(url)[2])
            lista[3].extend(obtenerDatos(url)[3])
        i=i+1
     
    return lista

def obtenerDatos(url):
    
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read().decode("utf-8"), 'html.parser')
    
    listaTitulo=[]
    listaFecha=[]
    listaEnlace=[]
    listaTexto=[]
    
    for noticia in soup.findAll("a",attrs={"class":"text-darker"}):
        tituloSinParsear=noticia.find("h2").string.strip()
        tituloParseado= eliminadorDiacriticos(tituloSinParsear)
        listaTitulo.append(tituloParseado)
        fechaSinParsear=(noticia.find("p").string.strip().split(" "))
        listaFecha.append(fechaSinParsear[0]+" "+fechaSinParsear[2])
        enlaceSinParsear=noticia.get("href")
        enlaceParseado= eliminadorDiacriticos(enlaceSinParsear)
        listaEnlace.append(enlaceParseado)
        for texto in noticia.findAll("p",attrs={"class":"newsItem__desc"}):
            textoSinParsear=texto.string.strip()
            textoParseado= eliminadorDiacriticos(textoSinParsear)
            listaTexto.append(textoParseado)
    
    return listaTitulo, listaFecha, listaEnlace, listaTexto

def crearTxt():
        
    lista = llamadaObtencionDatos()
    
    try:
        os.mkdir('Documentos')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    for i in range(0,len(lista[0])):

        file_object = open("Documentos\\Archivo"+str(i+1)+".txt","w",encoding="utf-8")
        file_object.write(str(lista[0][i]))
        file_object.write("\n")
        file_object.write(str(lista[1][i]))
        file_object.write("\n")
        file_object.write(str(lista[2][i]))
        file_object.write("\n")
        file_object.write(str(lista[3][i]))
        file_object.write("\n")


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
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " noticas")

    writer.commit()


def get_schema():
    return Schema( titulo=TEXT(stored=True),fecha=DATETIME(stored=True), enlace=TEXT(stored=True), resumen=TEXT(stored=True),nombrefichero=ID(stored=True) )


def add_doc(writer, path, docname):
    try:
        fileobj=open(path+'\\'+docname, "r")
        tit=fileobj.readline().strip()
        f=fileobj.readline().strip()
        fe=datetime2.strptime(f,'%d/%m/%Y %H:%M')
        enl=fileobj.readline().strip()
        res=fileobj.read()
        fileobj.close()           

    
        writer.add_document(titulo=tit, fecha=fe, enlace=enl, resumen=res,nombrefichero=docname)

        
        print("Creado indice para fichero " + docname)
    
    except:
        print("Error: No se ha podido anadir el documento "+path+'\\'+docname)

def apartado_b_a(dirindex):
    def mostrar_lista(event):
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            
            contenido=str(en.get()).split(" ")[0]
            operador=str(en.get()).split(" ")[1]
            titulo=str(en.get()).split(" ")[2]
            print(contenido)
            print(operador)
            print(titulo)
            
            if "Y" in operador:
                query=qparser.QueryParser('contenido',ix.schema, group=qparser.OrGroup).parse(contenido) & qparser.QueryParser('titulo',ix.schema , group=qparser.OrGroup).parse(titulo) 
            elif "OR" in operador:
                query=QueryParser('contenido',ix.schema).parse(contenido) | QueryParser('titulo',ix.schema).parse(titulo) 
            else:
                query=QueryParser('contenido',ix.schema).parse(contenido) -  QueryParser('titulo',ix.schema).parse(titulo) 
                
            
            results = searcher.search(query)


            imprimir_b_a(results)

    v = Toplevel()
    v.title("Busqueda por contenido  y/o/no titulo")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca contenido  Y/O/NO titulo :")
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
                fecha1 = fecha.split(" ")[0]
                fecha1Consulta = fecha1.split("/")[2]+fecha1.split("/")[1]+fecha1.split("/")[0] 
                fecha2 = fecha.split(" ")[1]
                if 'Dia' in fecha2:
                    
                    myquery='['+ fecha1Consulta + ' to ' +fecha1Consulta+']'
                    fecha2Consulta = fecha2.split("/")[2]+fecha2.split("/")[1]+fecha2.split("/")[0] 

                    print(myquery)
                query = QueryParser("fecha", ix.schema).parse(myquery)

                results = searcher.search(query)
                imprimir_b_b(results)
            except:
                print ("Error: Formato de fecha incorrecto")


    v = Toplevel()
    v.title("Busqueda por fecha ")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una fecha, siguiendo el patron (DD/MM/AAAA [Dia, Tarde]):")
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
            try:
                fecha = str(en2.get())
                titulo = str(en1.get()) 
                mparser = QueryParser('fecha',ix.schema).parse(fecha) | QueryParser('titulo',ix.schema).parse(titulo) 
           
                results = searcher.search(mparser)
                imprimir_b_b(results)
            except:
                print ("Error: Formato de fecha incorrecto")


    v = Toplevel()
    v.title("Busqueda por titulo y fecha")
    f1 =Frame(v)
    f1.pack(side=TOP)
    l1 = Label(f1, text="Introduzca un titulo :")
    l1.pack(side=LEFT)
    en1 = Entry(f1)
    en1.bind("<Return>", mostrar_lista)
    en1.pack(side=LEFT)
    f2 =Frame(v)
    f2.pack(side=TOP)
    l2 = Label(f2, text="Introduzca una fecha siguiendo el patron (AAAAMMDD) :")
    l2.pack(side=LEFT)
    en2 = Entry(f2)
    en2.bind("<Return>", mostrar_lista)
    en2.pack(side=LEFT)
      
def imprimir_b_c(results):
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

def ventanaBuscar():
    top = Tk()
    dirindex="Index"

    Buscar = Button(top, text="Contenido y Titulo ", command = lambda: apartado_b_a(dirindex))
    Buscar.pack(side = LEFT)

    fecha = Button(top, text="Fecha", command = lambda: apartado_b_b(dirindex))
    fecha.pack(side = LEFT)
    
    Buscar = Button(top, text="Titulo y Fecha ", command = lambda: apartado_b_c(dirindex))
    Buscar.pack(side = LEFT)



    top.mainloop()


def ventanaDatos():
    dirdocs="Documentos\\"
    dirindex="Index"
    top = Tk()
    indexar = Button(top, text="Cargar", command = lambda: apartado_a(dirdocs,dirindex))
    indexar.pack(side = LEFT)
    salir = Button(top, text= "Salir", command = quit)
    salir.pack(side = RIGHT)
    top.mainloop()

def ventanaPrincipal():
    top = Tk()
    dirdocs="Documentos\\"
    dirindex="Index"

    almacenarDatos = Button(top, text="Datos", command = ventanaDatos)
    almacenarDatos.pack(side = LEFT)

    buscarOfertas = Button(top, text="Buscar", command = ventanaBuscar)
    buscarOfertas.pack(side = RIGHT)

    top.mainloop()

if __name__ == '__main__':
    ventanaPrincipal()