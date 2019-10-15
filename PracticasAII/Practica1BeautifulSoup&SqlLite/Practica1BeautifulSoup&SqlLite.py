from bs4 import BeautifulSoup
import urllib.request as urllib2
import datetime
from tkinter import *
from tkinter import messagebox
import sqlite3

def obtenerDatos():
    url = "https://foros.derecho.com/foro/20-Derecho-Civil-General"
    response = urllib2.urlopen(url)
    webContent = response.read().decode('latin-1')
    soup = BeautifulSoup(webContent, 'html.parser')
    listadoTitulos=[]
    listadoEnlaces=[]
    listadoNombres=[]
    listadoFechas=[]
    listadoRespuestas=[]
    listadoVisitas=[]
   
    threads= soup.find(id="threads")
    for listaLi in threads.findAll("li"):
        for listaH3 in listaLi.findAll("h3"):
            listadoTitulos.append(listaH3.a.string)
            listadoEnlaces.append(url+str(listaH3.a.get('href')))
        autores2 = listaLi.findAll(class_="author")
        for i in autores2:
            nombres = str(i.find("a").string)
            listadoNombres.append(nombres)
            fechas = i.find("a").get("title").strip("Iniciado por "+str(i.find("a").string)+", el ")
            fechasCasting= datetime.datetime.strptime(fechas, '%d/%m/%Y %H:%M')
            listadoFechas.append(fechasCasting)
        for ul in listaLi.find_all(class_="threadstats td alt"):
            for contenido in ul.find_all("li"):
                if contenido.a != None:
                    listadoRespuestas.append("Respuestas: "+contenido.a.string)
                if "Visitas: " in contenido.get_text():
                    listadoVisitas.append(contenido.get_text())
                    
    return listadoTitulos, listadoEnlaces, listadoNombres,listadoFechas,listadoRespuestas,listadoVisitas    
    
def almacenar_bd():
    
    conn = sqlite3.connect('PRACTICA1.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS DERECHO")   
    conn.execute('''CREATE TABLE DERECHO
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
        TITULO           TEXT    NOT NULL,
        ENLACE           TEXT    NOT NULL,
        NOMBRE            TEXT NOT NULL,
        FECHA           DATATIME    NOT NULL,
        RESPUESTA           TEXT    NOT NULL,
        VISITA           TEXT    NOT NULL);''')
    
    l = obtenerDatos()
    
    i=0
    titulo=l[0]
    enlace=l[1]
    nombre=l[2]
    fecha=l[3]
    respuesta=l[4]
    visita=l[5]
    
    while i < len(titulo):
        
        conn.execute("""INSERT INTO DERECHO (TITULO, ENLACE, NOMBRE, FECHA, RESPUESTA, VISITA) VALUES (?,?,?,?,?,?)""",(titulo[i],enlace[i],nombre[i], fecha[i], respuesta[i], visita[i]))
        i=i+1

    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM DERECHO")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()

def listar_bd():
    conn = sqlite3.connect('PRACTICA1.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO,NOMBRE,FECHA FROM DERECHO")
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

def imprimir_etiqueta2(cursor):
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

def buscar_bdTema():
    def listar_busquedaTema(event):
        conn = sqlite3.connect('PRACTICA1.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT TITULO,NOMBRE,FECHA FROM DERECHO WHERE TITULO LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Introduzca tema: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busquedaTema)
    en.pack(side = LEFT)
    
def buscar_bdFecha():
    def listar_busquedaFecha(event):
        conn = sqlite3.connect('PRACTICA1.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT TITULO,NOMBRE,FECHA FROM DERECHO WHERE FECHA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Introduzca fecha(YYYY-MM-dd): ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busquedaFecha)
    en.pack(side = LEFT)
    
def listar_Popu():
    conn = sqlite3.connect('PRACTICA1.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO,NOMBRE,FECHA,VISITA FROM DERECHO order by VISITA desc LIMIT 5" )
    imprimir_etiqueta2(cursor)
    conn.close()
    
def listar_Activos():
    conn = sqlite3.connect('PRACTICA1.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO,NOMBRE,FECHA,RESPUESTA FROM DERECHO order by RESPUESTA desc LIMIT 5")
    imprimir_etiqueta2(cursor)
    conn.close()
    

def ventanaPrincipal():
    top = Tk()
    almacenar = Button(top, text="Datos", command = ventanaDatos)
    almacenar.pack(side = LEFT)
    
    buscar= Button(top, text="Buscar", command = ventanaBuscar)
    buscar.pack(side = LEFT)
    
    estadistica = Button(top, text="Estadisticas", command =ventanaEstadistica)
    estadistica.pack(side = LEFT)
    
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
    tema = Button(top, text="Tema", command = buscar_bdTema)
    tema.pack(side = LEFT)
    
    fecha = Button(top, text="Fecha", command = buscar_bdFecha)
    fecha.pack(side = LEFT)
    
    Salir = Button(top, text="Salir", command =quit)
    Salir.pack(side = LEFT)
    top.mainloop()

def ventanaEstadistica():
    top = Tk()
    Populares = Button(top, text="Populares", command = listar_Popu)
    Populares.pack(side = LEFT)
    
    Activos = Button(top, text="Activos", command = listar_Activos)
    Activos.pack(side = LEFT)
    
    Salir = Button(top, text="Salir", command =quit)
    Salir.pack(side = LEFT)
    top.mainloop()
    

if __name__ == "__main__":
    ventanaPrincipal()
