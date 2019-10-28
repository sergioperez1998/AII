import urllib.request, re
from tkinter import *
from tkinter import messagebox
import sqlite3
import os
from bs4 import BeautifulSoup
    
def obtencionNoticias():
    
    response = urllib.request.urlopen('http://www.us.es/rss/feed/portada')
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    listado_title=[]
    listado_link=[]
    listado_fechaNoFormateada=[]
    for titulo in soup.find_all("title"):
        listado_title.append(titulo.string)
    #Lo hacemos con expresiones logicas porque dan conflictos con el html parser
    for links in re.findall("<link>(.+)</link>",html):
        listado_link.append(links)
    for fecha in soup.find_all(re.compile("pub")):
        listado_fechaNoFormateada.append(fecha.string)
    listado_fecha = formateoFecha(listado_fechaNoFormateada)
    return listado_title,listado_link,listado_fecha
    
def formateoFecha(l1):
    
    res=[]
    diccionarioMeses={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    for fecha in l1:
        dia = fecha.split(" ")[1]
        ano = fecha.split(" ")[3]
        mesNoFormatado = fecha.split(" ")[2]
        mes= diccionarioMeses[mesNoFormatado]
        res.append(dia+"/"+mes+"/"+ano)
    return res

def almacenar_bd():
    
    conn = sqlite3.connect('Ejercicio3.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS NOTICIAS")   
    conn.execute('''CREATE TABLE NOTICIAS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       TITULO           TEXT    NOT NULL,
       LINK           TEXT    NOT NULL,
       FECHA        TEXT NOT NULL);''')
    
    l = obtencionNoticias()
    
    i=0
    titulos=l[0]
    links=l[1]
    fechas=l[2]
    while i < len(titulos):
        
        conn.execute("""INSERT INTO NOTICIAS (TITULO, LINK, FECHA) VALUES (?,?,?)""",(titulos[i],links[i],fechas[i]))
        i=i+1

    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM NOTICIAS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
def listar_bd():
    conn = sqlite3.connect('Ejercicio3.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO,LINK, FECHA FROM NOTICIAS")
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

def buscar_bd():
    def listar_busqueda(event):
        conn = sqlite3.connect('Ejercicio3.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT TITULO,LINK,FECHA FROM NOTICIAS WHERE FECHA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Introduzca el mes (Numero de mes): ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)


def ventanaPrincipal():
    top = Tk()
    almacenar = Button(top, text="Almacenar", command = almacenar_bd)
    almacenar.pack(side = LEFT)
    listar = Button(top, text="Listar", command = listar_bd)
    listar.pack(side = LEFT)
    Buscar = Button(top, text="Buscar", command = buscar_bd)
    Buscar.pack(side = LEFT)
    top.mainloop()
    
if __name__ == "__main__":
    ventanaPrincipal()




