'''
Created on 24 oct. 2019

@author: sergi
'''
#Esto son los imports:
encoding = "utf-8"
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import datetime
from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import ttk

#Metodo para el scraping:

def obtencionDatos():
    
    url = "https://www.ulabox.com/campaign/productos-sin-gluten#gref"
    response = urllib2.urlopen(url)
    webContent = response.read()
    soup = BeautifulSoup(webContent, 'html.parser')
    
    listadaA=[]
    listadoB=[]
    listadoC=[]
    listadoD=[]
    listadoE=[]
    
#Metodo de almacenado en la bd:

def almacenar_bd():
    
    conn = sqlite3.connect('EXAMEN1.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS ZAPATILLAS")   
    conn.execute('''CREATE TABLE ZAPATILLAS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
        NOMBRE           TEXT    NOT NULL,
        MARCA           TEXT    NOT NULL,
        PRECIO           TEXT NOT NULL,
        PRECIOOFERTA        TEXT,
        ESTRELLAS         TEXT NOT NULL,
        PUNTUACIONES        INTEGER);''')
    
    l = obtencionDatos()
    
    i=0
    nombre=l[0]
    marca=l[1]
    precio=l[2]
    precioOferta=l[3]
    estrellas=l[4]
    puntuaciones=l[5]
   
    
    while i < len(nombre):
        
        conn.execute("""INSERT INTO ZAPATILLAS (NOMBRE, MARCA, PRECIO, PRECIOOFERTA, ESTRELLA, PUNTUACION) VALUES (?,?,?,?,?,?)""",(nombre[i],marca[i],precio[i], precioOferta[i], estrellas[i], puntuaciones[i]))
        i=i+1

    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM ZAPATILLAS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()

def imprimir_etiqueta(cursor):
    
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,+row[1])
        lb.insert(END,+row[2])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)    
    
#VENTANA PRINCIPAL:

def ventanaPrincipal():
    top = Tk()

    almacenarDatos = Button(top, text="Datos", command = ventanaDatos)
    almacenarDatos.pack(side = LEFT)

    buscarOfertas = Button(top, text="Buscar", command = ventanaBuscar)
    buscarOfertas.pack(side = RIGHT)

    top.mainloop()

def ventanaDatos():
    top = Tk()

    cargarDatos = Button(top, text="Cargar", command = almacenar_bd)
    cargarDatos.pack(side = LEFT)

    salir = Button(top, text= "Salir", command = ventanaPrincipal)
    salir.pack(side = RIGHT)

    top.mainloop()

def ventanaBuscar():
    top = Tk()

    nombre = Button(top, text="Nombre", command = ventanaNombre)
    nombre.pack(side = LEFT)

    ordenarPuntuacion = Button(top, text="ORdenar por Puntuación", command = ventanaOrdenar)
    ordenarPuntuacion.pack(side = LEFT)

    marcas = Button(top, text="Marcas", command = ventanaMarcas)
    marcas.pack(side = RIGHT)

    top.mainloop()

def ventanaNombre():
    def buscarNombre():
        conn = sqlite3.connect('EXAMEN1.db')
        conn.text_factory = str
        s = "%"+entry.get()+"%" 
        cursor = conn.execute("""SELECT NOMBRE,MARCA,PRECIO FROM ZAPATILLAS WHERE NOMBRE LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()

    top = Tk()

    L1 = Label(top, text="Introduzca un nombre:")
    L1.pack(side=LEFT)
    entry = Entry(top, bd = 5)
    entry.bind("<Return>", buscarNombre)
    entry.pack(side = RIGHT)

    top.mainloop()

def ventanaOrdenar():
    conn = sqlite3.connect('EXAMEN1.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT NOMBRE,PRECIO,PUNTUACION FROM ZAPATILLAS WHERE PUNTUACION > 5 ORDER BY ASC""")
    imprimir_etiqueta(cursor)
    conn.close()

def ventanaMarcas():
    def listarMarcas():
        conn = sqlite3.connect('EXAMEN1.db')
        conn.text_factory = str  
        s = spinbox.get()
        cursor = conn.execute("""SELECT NOMBRE,MARCA,PRECIO,PUNTUACION FROM ZAPATILLAS WHERE MARCA = ?""",(s,))
        imprimir_etiquetaMarcas(cursor)
        conn.close()

    listaMarcasCursor=[]
    conn = sqlite3.connect('EXAMEN1.db')
    cursor = conn.execute("SELECT DISTINCT MARCA FROM ZAPATILLAS")
    listaMarcasCursor= [x[0] for x in cursor]
    master = Tk()
    spinbox=ttk.Spinbox(master, values=listaMarcasCursor,  state='readonly') 
    spinbox.grid(column=1, row=0, padx=10, pady=10)
    boton=ttk.Button(master, text="Seleccionar", command=listarMarcas)
    boton.grid(column=0, row=1, padx=10, pady=10)

def imprimir_etiquetaMarcas(cursor):
    
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,row[3])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)

#PARA REALIZAR LA LLAMADA A LA VENTANA PRINCIPAL:

if __name__ == "__main__":
    ventanaPrincipal()


