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
import errno




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
    
    soup = BeautifulSoup(response.read().decode("latin-1"), 'lxml')
    
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


def ventanaDatos():
    dirdocs="Txts"
    dirindex="Index"
    top = Tk()

    cargarDatos = Button(top, text="Cargar", command = lambda: (dirdocs,dirindex))
    cargarDatos.pack(side = LEFT)

    salir = Button(top, text= "Salir", command = quit)
    salir.pack(side = RIGHT)

    top.mainloop()

def ventanaBuscar():
    top = Tk()

    tituloYDescripcion = Button(top, text="Titulo y Descripcion", command = ventanaTituloYDescripcion)
    tituloYDescripcion.pack(side = LEFT)

    fecha = Button(top, text="Fecha", command = ventanaFecha)
    fecha.pack(side = LEFT)

    descripcion = Button(top, text="Descripcion", command = ventanaDescripcion)
    descripcion.pack(side = RIGHT)

    top.mainloop()

def ventanaTituloYDescripcion():
    def buscarNoticias(event):
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)

        s = entry.get() #s es lo que escribe el usuario
        
    top = Tk()

    L1 = Label(top, text="Introduzca una o varias palabras:")
    L1.pack(side=LEFT)
    entry = Entry(top, bd = 5)
    entry.bind("<Return>", buscarNoticias)
    entry.pack(side = RIGHT)

    top.mainloop()

def ventanaFecha():
    def buscarNoticiasFecha():
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)

        s1 = entry1.get()
        s2 = entry2.get() #s1 y s2 son los valores de las fechas en formato DD/MM/AAAA
        
    top = Tk()

    L1 = Label(top, text="Introduzca un rango de fechas en formato DD/MM/AAAA:")
    L2 = Label(top, text="-")
    L1.pack(side=LEFT)
    entry1 = Entry(top, bd = 5)
    entry2 = Entry(top, bd = 5)
    button = Button(top, text = "Buscar", command = buscarNoticiasFecha)
    entry1.pack(side = LEFT)
    L2.pack(side = LEFT)
    entry2.pack(side = LEFT)
    button.pack(RIGHT)

    top.mainloop()

def ventanaDescripcion():
    def buscarNoticias(event):
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)

        s = entry.get() #s es lo que escribe el usuario
        
    top = Tk()

    L1 = Label(top, text="Introduzca una frase:")
    L1.pack(side=LEFT)
    entry = Entry(top, bd = 5)
    entry.bind("<Return>", buscarNoticias)
    entry.pack(side = RIGHT)

    top.mainloop()
        
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
        a = lista[4][i]
        b = str(a)
        file_object.write(b)        
    
def ventana_principal():
    top = Tk()
    datos = Button(top, text="Datos", command = ventanaDatos)
    datos.pack(side = LEFT)
    buscar = Button(top, text="Buscar", command = ventanaBuscar)
    buscar.pack(side = RIGHT)
    top.mainloop()

if __name__ == '__main__':
    ventana_principal() 


crearTxt()