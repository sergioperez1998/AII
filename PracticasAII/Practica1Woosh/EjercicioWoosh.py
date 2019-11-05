encoding:'utf-8'
from bs4 import BeautifulSoup
import urllib.request as urllib2
import datetime
from tkinter import *
from tkinter import messagebox
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser
import datetime
import calendar
import urllib.request
import locale; 
import re
from unicodedata import normalize

def obtenerDatos():
    
    url = "https://foros.derecho.com/foro/34-Derecho-Inmobiliario"
    response = urllib2.urlopen(url)
    webContent = response.read()
    soup = BeautifulSoup(webContent, 'html.parser')
    
    listadoTitulosTema=[]
    listadoEnlacesTema=[]
    listadoNombresTema=[]
    listadoFechasTema=[]
    listadoRespuestasTema=[]
    listadoVisitasTema=[]
   
    threads= soup.find(id="threads")
    for listaLi in threads.findAll("li"):
        for listaH3 in listaLi.findAll("h3"):
            listadoTitulosTema.append(listaH3.a.string)
            listadoEnlacesTema.append(url+str(listaH3.a.get('href')))
        autores2 = listaLi.findAll(class_="author")
        for i in autores2:
            nombres = str(i.find("a").string)
            listadoNombresTema.append(nombres)
            fechas = i.find("a").get("title").strip("Iniciado por "+str(i.find("a").string)+", el ")
            if "Ayer " in fechas:
                ahora = datetime.datetime.utcnow()
                ayer = ahora - datetime.timedelta(days=1)
                fechaDeAyer = str(ayer.day)+"/"+str(ayer.month)+'/'+str(ayer.year)+' '+fechas.strip("Ayer ")
                fechasCasting= datetime.datetime.strptime(fechaDeAyer, '%d/%m/%Y %H:%M')
                listadoFechasTema.append(fechasCasting)
            else:
                fechasCasting= datetime.datetime.strptime(fechas, '%d/%m/%Y %H:%M')
                listadoFechasTema.append(fechasCasting)
        for ul in listaLi.find_all(class_="threadstats td alt"):
            for contenido in ul.find_all("li"):
                if contenido.a != None:
                    listadoRespuestasTema.append("Respuestas: "+contenido.a.string)
                if "Visitas: " in contenido.get_text():
                    listadoVisitasTema.append(contenido.get_text())
                    
    for enlace in listadoEnlacesTema:
    
        s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize("NFD", enlace), 0, re.I)
   
        s = normalize('NFC', s)
        print(s)
        response = urllib2.urlopen(s)
        webContent = response.read()
        soup2 = BeautifulSoup(webContent, 'html.parser')
   
print(obtenerDatos())