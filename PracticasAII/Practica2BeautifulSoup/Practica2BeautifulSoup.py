encoding = "utf-8"
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import datetime
from tkinter import *
import sqlite3
from tkinter import messagebox

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
    
    return listadoMarcas,listadoNombres,listadoLinks,listadoPrecioActual,listadoPrecioSinOferta
   
           
def ventanaPrincipal():
    top = Tk()

    almacenarDatos = Button(top, text="Almacenar datos", fg = "Green", command = almacenar_bd)
    almacenarDatos.pack(side = LEFT)

    mostrarMarca = Button(top, text="Mostrar marca", fg = "Purple", command = seleccionar_marca)
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
def almacenar_bd():
    
    conn = sqlite3.connect('PRACTICA2.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS ALIMENTOS")   
    conn.execute('''CREATE TABLE ALIMENTOS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
        MARCA           TEXT    NOT NULL,
        NOMBRE           TEXT    NOT NULL,
        LINK           TEXT NOT NULL,
        PRECIOACTUAL        TEXT   NOT NULL,
        PRECIOSINOFERTA         TEXT    );''')
    
    l = obtencionDatos()
    
    i=0
    marca=l[0]
    nombre=l[1]
    link=l[2]
    precioActual=l[3]
    precioSinOferta=l[4]
   
    
    while i < len(marca):
        
        conn.execute("""INSERT INTO ALIMENTOS (MARCA, NOMBRE, LINK, PRECIOACTUAL, PRECIOSINOFERTA) VALUES (?,?,?,?,?)""",(marca[i],nombre[i],link[i], precioActual[i], precioSinOferta[i]))
        i=i+1

    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM ALIMENTOS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
def seleccionar_marca():
    l = obtencionDatos()
    marcas=l[0]
    master = Tk()
    marca = Spinbox(master, values=marcas)
    marca.pack()
    boton1=Button(master, text="Seleccionar", command=listar_bd(marca.get()))
    boton1.pack(side = LEFT)
    master.mainloop()
    

def listar_bd(marca):
        
          
        conn = sqlite3.connect('PRACTICA2.db')
        conn.text_factory = str  
        
        cursor = conn.execute("""SELECT NOMBRE,PRECIOACTUAL FROM ALIMENTOS WHERE MARCA = ?""",(marca,))
        imprimir_etiqueta(cursor)
        conn.close()
    
    
    
    
    
def imprimir_etiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)


if __name__ == "__main__":
    ventanaPrincipal()
    

