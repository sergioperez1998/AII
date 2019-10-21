from bs4 import BeautifulSoup
import urllib.request as urllib2
import datetime
from tkinter import *
import sqlite3

def ventanaPrincipal():
    top = Tk()

    almacenarDatos = Button(top, text="Almacenar datos", fg = "Green", command = obtenerDatos)
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