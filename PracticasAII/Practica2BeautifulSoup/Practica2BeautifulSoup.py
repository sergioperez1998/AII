encoding = "utf-8"
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import datetime
from tkinter import *
import sqlite3

def obtencionDatos():
    
    url = "https://www.ulabox.com/campaign/productos-sin-gluten#gref"
    urlConcatenacion="https://www.ulabox.com"
    response = urllib2.urlopen(url)
    webContent = response.read()
    soup = BeautifulSoup(webContent, 'html.parser')
    listadoMarcas=[]
    listadoLinks=[]
    listadoNombres=[]
    listadoPrecioActual=[]
    listadoPrecioSinOferta=[]
    for claseIslet in soup.findAll(class_ = "islet"):
        for claseIsletH4 in claseIslet.findAll("h4"):
            listadoMarcas.append((claseIsletH4.a.get_text().strip()))
        for claseIsletH3 in claseIslet.findAll("h3"):
            listadoLinks.append(urlConcatenacion+claseIsletH3.a.get("href"))
            listadoNombres.append(claseIsletH3.a.get_text().strip())
    for pie in soup.findAll(class_="product-grid-footer__price"):
        PrecioTotal=""
        for allSpan in pie.findAll("span"):
            precio1=allSpan.get_text()
            PrecioTotal=PrecioTotal+precio1
        listadoPrecioActual.append(PrecioTotal)
        
        precioSinOferta= None
        
        try:
            precioSinOferta = pie.find("del").string
        except:
            precioSinOferta = None
        
        if(precioSinOferta!=None):
            m=re.compile('.*(\d+,\d+).*').match(precioSinOferta)
            precioSinOferta= m.groups(1)[0]
        listadoPrecioSinOferta.append(precioSinOferta)
    
    print(listadoMarcas)
    print(listadoLinks)
    print(listadoNombres)
    print(listadoPrecioActual)
    print(listadoPrecioSinOferta)
           
def ventanaPrincipal():
    top = Tk()

    almacenarDatos = Button(top, text="Almacenar datos", fg = "Green", command = obtencionDatos)
    almacenarDatos.pack(side = LEFT)

    mostrarMarca = Button(top, text="Mostrar marca", fg = "Purple", command = obtenerMarca)
    mostrarMarca.pack(side = LEFT)

    buscarOfertas = Button(top, text="Buscar ofertas", fg = "Blue", command = obtenerOferta)
    buscarOfertas.pack(side = RIGHT)

    top.mainloop()

def obtenerDatos():
    top = Tk()

    top.mainloop()

def obtenerMarca():
    top = Tk()

    top.mainloop()

def obtenerOferta():
    top = Tk()

    scrollbar = Scrollbar(top)
    scrollbar.pack( side = RIGHT, fill = Y )

    listbox = Listbox(top, yscrollcommand = scrollbar.set)

    conn = sqlite3.connect('PRACTICA2.db')
    cursor = conn.execute("SELECT NOMBRE,PRECIOSINOFERTA,PRECIOCONOFERTA FROM OFERTA WHERE PRECIOSINOFERTA NOT NULL")

    for row in cursor:
        index = 1
        listbox.insert(index,row)
        index = index + 1

    listbox.pack()
    scrollbar.config(command = listbox.yview)

    top.mainloop()

if __name__ == "__main__":
    ventanaPrincipal()
