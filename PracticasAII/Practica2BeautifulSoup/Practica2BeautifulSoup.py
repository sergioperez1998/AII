from bs4 import BeautifulSoup
import urllib.request as urllib2
import datetime
from tkinter import *
import sqlite3

def ventanaPrincipal():
    top = Tk()

    almacenarDatos = Button(top, text="Almacenar datos", command = obtenerDatos)
    almacenarDatos.pack(side = LEFT)

    mostrarMarca = Button(top, text="Mostrar marca", command = obtenerMarca)
    mostrarMarca.pack(side = LEFT)

    buscarOfertas = Button(top, text="Buscar ofertas", command = obtenerOferta)
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
    listbox.insert(1, "Python")
    listbox.insert(2, "Perl")
    listbox.insert(3, "C")
    listbox.insert(4, "PHP")
    listbox.insert(5, "JSP")
    listbox.insert(6, "Ruby")
    listbox.insert(7, "Prueba1")
    listbox.insert(8, "Prueba2")
    listbox.insert(9, "Prueba3")
    listbox.insert(10, "Prueba4")
    listbox.insert(11, "Prueba5")
    listbox.insert(12, "Prueba6")

    listbox.pack()
    scrollbar.config(command = listbox.yview)

    top.mainloop()

if __name__ == "__main__":
    ventanaPrincipal()