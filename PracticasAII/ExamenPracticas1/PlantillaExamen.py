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
    conn.execute("DROP TABLE IF EXISTS EXAMEN")   
    conn.execute('''CREATE TABLE EXAMEN
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
        A           TEXT    NOT NULL,
        B           TEXT    NOT NULL,
        C           TEXT NOT NULL,
        D        TEXT   NOT NULL,
        E         TEXT    );''')
    
    l = obtencionDatos()
    
    i=0
    A=l[0]
    B=l[1]
    C=l[2]
    D=l[3]
    E=l[4]
   
    
    while i < len(A):
        
        conn.execute("""INSERT INTO EXAMEN1 (A, B, C, D, E) VALUES (?,?,?,?,?)""",(A[i],B[i],C[i], D[i], E[i]))
        i=i+1

    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM EXAMEN1")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
#PARA LISTADOS NORMALES:

def listar_bd():
    conn = sqlite3.connect('EXAMEN1.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT A,B,C FROM EXAMEN1")
    imprimir_etiqueta(cursor)
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
    
#PARA LOS BUSCAR NORMALES:

def buscar_bdTema():
    def listar_busquedaTema(event):
        conn = sqlite3.connect('EXAMEN1.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT A,B,C FROM EXAMEN1 WHERE TITULO LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Introduzca tema: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busquedaTema)
    en.pack(side = LEFT)    
    

#VENTANA PRINCIPAL:

def ventanaPrincipal():
    top = Tk()

    almacenarDatos = Button(top, text="ACCION1", fg = "Green", command = A)
    almacenarDatos.pack(side = LEFT)

    mostrarMarca = Button(top, text="ACCION2", fg = "Purple", command = B)
    mostrarMarca.pack(side = LEFT)

    buscarOfertas = Button(top, text="ACCION3", fg = "Blue", command = C)
    buscarOfertas.pack(side = RIGHT)

    top.mainloop()

#PARA REALIZAR LA LLAMADA A LA VENTANA PRINCIPAL:
'''
if __name__ == "__main__":
    ventanaPrincipal()
'''

