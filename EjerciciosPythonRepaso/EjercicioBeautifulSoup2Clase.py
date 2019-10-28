encoding="utf-8"
from bs4 import BeautifulSoup
import urllib.request
import urllib.request as urllib2
import datetime
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk

def llamadaObtencionDatos():
    
    i=1
    lista=[]
    
    while i<4:
        url="https://www.meneame.net/?page="+str(i)
        if i == 1:
            lista=obtencionDatos(url)
        else:
            lista[0].extend(obtencionDatos(url)[0])
            lista[1].extend(obtencionDatos(url)[1])
            lista[2].extend(obtencionDatos(url)[2])
            lista[3].extend(obtencionDatos(url)[3])
            lista[4].extend(obtencionDatos(url)[4])
        i=i+1
     
    return lista
    
def obtencionDatos(url):
    
    
    response = urllib2.urlopen(url)
    webContent = response.read()
    soup = BeautifulSoup(webContent, 'html.parser')
    
    listaTitulos=[]
    listaLinks=[]
    listaNombres = []
    listaFechas=[]
    listaContenido=[]
    

    for claseCenterContect in soup.findAll(class_="center-content"):
        listaTitulos.append(claseCenterContect.h2.a.get_text())
        listaLinks.append(claseCenterContect.h2.a.get("href"))
        for claseNewsSubmitted in claseCenterContect.findAll(class_="news-submitted"):
            listaNombres.append(claseNewsSubmitted.a.get("href").split("/")[2])
            for claseVisible in claseNewsSubmitted.findAll("span", attrs={"class":"ts visible"}):
                if "publicado:" in claseVisible.get("title").strip(): 
                    fechaFormatear= int(claseVisible.get("data-ts"))
                    fechaFormateada= datetime.fromtimestamp(fechaFormatear)
                    listaFechas.append(fechaFormateada)
                '''
                Tengo que sacar el data-ts y formatear la fecha
                timestamp = 1545730073
                dt_object = datetime.fromtimestamp(timestamp)
                '''
        for descripcion in claseCenterContect.findAll("div",attrs={"class":"news-content"}):
            listaContenido.append(descripcion.get_text())
            
    listaDatos= [listaTitulos, listaLinks, listaNombres, listaFechas,listaContenido]
    return listaDatos


def almacenar_bd():
    
    conn = sqlite3.connect('EjercicioBS2.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS ANUNCIOS")   
    conn.execute('''CREATE TABLE ANUNCIOS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
        TITULO           TEXT    NOT NULL,
        LINK           TEXT    NOT NULL,
        NOMBRE            TEXT NOT NULL,
        FECHA           DATATIME    NOT NULL,
        CONTENIDO           TEXT    NOT NULL);''')
    
    l = llamadaObtencionDatos()
    print(l)
    i=0
    titulo=l[0]
    link=l[1]
    nombre=l[2]
    fecha=l[3]
    contenido=l[4]
    
    while i < len(titulo):
        
        conn.execute("""INSERT INTO ANUNCIOS (TITULO, LINK, NOMBRE, FECHA, CONTENIDO) VALUES (?,?,?,?,?)""",(titulo[i],link[i],nombre[i], fecha[i], contenido[i]))
        i=i+1

    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM ANUNCIOS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
def listar_bd():
    conn = sqlite3.connect('EjercicioBS2.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO,NOMBRE,FECHA FROM ANUNCIOS")
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
        lb.insert(END,row[2])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)
    
def seleccionar_nombre():
    
    def listarNombres():
     
        conn = sqlite3.connect('EjercicioBS2.db')
        conn.text_factory = str  
        s = spinbox.get()
        cursor = conn.execute("""SELECT TITULO,NOMBRE,FECHA FROM ANUNCIOS WHERE NOMBRE= ?""",(s,))
        imprimir_etiqueta(cursor)
        conn.close()
    
    listaNombreCursor=[]
    conn = sqlite3.connect('EjercicioBS2.db')
    cursor = conn.execute("SELECT DISTINCT NOMBRE FROM ANUNCIOS")
    listanNombreCursor= [x[0] for x in cursor]
    master = Tk()
    spinbox=ttk.Spinbox(master, values=listanNombreCursor,  state='readonly') 
    spinbox.grid(column=1, row=0, padx=10, pady=10)
    boton=ttk.Button(master, text="Seleccionar", command=listarNombres)
    boton.grid(column=0, row=1, padx=10, pady=10)

def buscar_bdFecha():
    def listar_busquedaFecha(event):
        conn = sqlite3.connect('EjercicioBS2.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT TITULO,NOMBRE,FECHA FROM ANUNCIOS WHERE FECHA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Introduzca fecha(YYYY-MM-dd): ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busquedaFecha)
    en.pack(side = LEFT)
    
def ventanaPrincipal():
    top = Tk()
    almacenar = Button(top, text="Datos", command = ventanaDatos)
    almacenar.pack(side = LEFT)
    
    buscar= Button(top, text="Buscar", command = ventanaBuscar)
    buscar.pack(side = LEFT)   
    
    top.mainloop()
def ventanaDatos():
    top = Tk()
    almacenar = Button(top, text="Cargar", command = almacenar_bd)
    almacenar.pack(side = LEFT)
    
    listar = Button(top, text="Mostrar", command = listar_bd)
    listar.pack(side = LEFT)
    
    Salir = Button(top, text="Salir", command =quit)
    Salir.pack(side = LEFT)
    top.mainloop()

def ventanaBuscar():
    top = Tk()
    tema = Button(top, text="Autor", command = seleccionar_nombre)
    tema.pack(side = LEFT)
    
    fecha = Button(top, text="Fecha", command = buscar_bdFecha)
    fecha.pack(side = LEFT)
    
    Salir = Button(top, text="Salir", command =quit)
    Salir.pack(side = LEFT)
    
    top.mainloop()
    
if __name__ == "__main__":
    ventanaPrincipal()