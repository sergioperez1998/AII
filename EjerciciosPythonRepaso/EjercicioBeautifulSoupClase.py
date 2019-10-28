encoding="latin-1"
from bs4 import BeautifulSoup
import urllib.request as urllib2
import datetime
from tkinter import *
from tkinter import messagebox
import sqlite3

def obtencionDatos():
    
    url = "https://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/"
    urlBasica ="https://resultados.as.com/"
    response = urllib2.urlopen(url)
    webContent = response.read()
    soup = BeautifulSoup(webContent, 'html.parser')
    listaNombres=[]
    listaUrls = []
    listaResultados=[]
    for claseJornada in soup.findAll(class_="cont-modulo resultados"):
        for claseResultado in claseJornada.findAll(class_="resultado"):
            listaUrls.append(urlBasica+claseResultado.get("href"))
            listaResultados.append(claseResultado.get_text().strip())
            nombre=claseResultado.get("title").strip(" en directo")
            listaNombres.append(nombre)
    return listaNombres,listaResultados,listaUrls

def almacenar_bd():
    
    conn = sqlite3.connect('EjercicioClaseBeautiful.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS PERIODICO")   
    conn.execute('''CREATE TABLE PERIODICO
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
        NOMBRE           TEXT    NOT NULL,
        RESULTADO           TEXT    NOT NULL,
        URL           TEXT    NOT NULL);''')
    
    l = obtencionDatos()
    
    i=0
    nombre=l[0]
    resultado=l[1]
    url=l[2]
    
    while i < len(nombre):
        
        conn.execute("""INSERT INTO PERIODICO (NOMBRE, RESULTADO, URL) VALUES (?,?,?)""",(nombre[i],resultado[i],url[i]))
        i=i+1

    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PERIODICO")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
def listar_bd():
    conn = sqlite3.connect('EjercicioClaseBeautiful.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT NOMBRE,RESULTADO,URL FROM PERIODICO")
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
    
def ventanaPrincipal():
    top = Tk()
    almacenar = Button(top, text="Datos", command = almacenar_bd)
    almacenar.pack(side = LEFT)
    
    listar= Button(top, text="Listar", command =  listar_bd)
    listar.pack(side = LEFT)
    
    Salir = Button(top, text="Salir", command =quit)
    Salir.pack(side = LEFT)
    
    top.mainloop()
    
if __name__ == "__main__":
    ventanaPrincipal()
