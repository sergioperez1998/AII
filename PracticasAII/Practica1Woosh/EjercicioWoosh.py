encoding = "utf-8"
from bs4 import BeautifulSoup
import urllib.request
import datetime
from tkinter import *
from tkinter import messagebox
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
import os, os.path
from whoosh import index,fields
from unicodedata import normalize
import errno


def obtenerDatos():
    
    url = "https://foros.derecho.com/foro/34-Derecho-Inmobiliario"
    urlBasica = "https://foros.derecho.com/"
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read().decode("latin-1"), 'lxml')
    
    listaTitulo=[]
    listaLink=[]
    listaAutor=[]
    listaFecha=[]
    listaRespuesta=[]
    listaVisita=[]
    
    listaContenido1=[]
    listaContenido2=[]
    
    
    for titleLink in soup.findAll("div",attrs={"class":"inner"}):
        listaTitulo.append(titleLink.a.string)
        listaLink.append(urlBasica+titleLink.a.get("href"))
        for AutorFecha in soup.findAll("div",attrs={"class":"author"}):
            fecha = AutorFecha.find("span")
            fechaSinCasting=fecha.get_text().split(",")[1].strip()
            fechaCasting= datetime.datetime.strptime(fechaSinCasting, '%d/%m/%Y %H:%M')
            listaFecha.append(fechaCasting)
            listaAutor.append(AutorFecha.a.string)
    for RespuestaCalificacion in soup.findAll("ul",attrs={"class":"threadstats td alt"}):
        listaRespuesta.append(str(RespuestaCalificacion.a.string))
        for lis in RespuestaCalificacion.findAll("li"):
            if "Visitas: " in lis.get_text():
                listaVisita.append(str(lis.get_text().split(" ")[1]))
    
    
    listaLinkRespuesta=[]
    listaFechaRespuesta=[]
    listaTextoRespuesta=[]
    listaAutorRespuesta=[]
    
    
    for enlace in listaLink:
        
        s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize("NFD", enlace), 0, re.I)
        s = normalize('NFC', s)
        
        response2 = urllib.request.urlopen(s)
        soup2 = BeautifulSoup(response2.read().decode("latin-1"), 'lxml')
        
        listaLinkRespuesta.append(enlace)
        
        i=0
        fechasRespuesta=[]
        for date in soup2.findAll("div",attrs={"class":"posthead"}):
            
            
            fecha = date.span.get_text().split(",")
            fechaCompleta= fecha[0] + fecha[1]
            fechaSinCasting2=fechaCompleta.strip()
            fechaCasting2= datetime.datetime.strptime(fechaSinCasting2, '%d/%m/%Y %H:%M')
            
            if i != 0:
                fechasRespuesta.append(fechaCasting2)
                i=i+1
            else:
                i=i+1
        listaFechaRespuesta.append(fechasRespuesta)
        
        indice=0
        textoRespuesta=[]                                                                  
        for txt in soup2.findAll("div",attrs={"class":"content"}):
            
            texto=txt.blockquote.string
            if indice!=0:
                if "NoneType" in type(texto).__name__:
                    textoRespuesta.append(None)
                    indice=indice+1
                else:
                    textoParseado= texto.strip()
                    textoRespuesta.append(textoParseado)
                    indice=indice+1
            else:
                indice=indice+1
        listaTextoRespuesta.append(textoRespuesta)
        
        indice1=0
        autorRespuesta=[]
        for autor in soup2.findAll("div",attrs={"class":"popupmenu memberaction"}):
            
            if indice1!=0:
                autorRespuesta.append(autor.strong.string)
                indice1=indice1+1
            else:
                indice1=indice1+1
        listaAutorRespuesta.append(autorRespuesta)
        
    listaContenido1.append(listaTitulo)
    listaContenido1.append(listaLink)
    listaContenido1.append(listaAutor)
    listaContenido1.append(listaFecha)
    listaContenido1.append(listaRespuesta)
    listaContenido1.append(listaVisita)
    
    listaContenido2.append(listaLinkRespuesta)
    listaContenido2.append(listaFechaRespuesta)
    listaContenido2.append(listaTextoRespuesta)
    listaContenido2.append(listaAutorRespuesta)
    
    return listaContenido1, listaContenido2


def crearTxt():
    
    lista = obtenerDatos()
    
    listaContenido1=lista[0]
    listaContenido2=lista[1]
    
    try:
        os.mkdir('Publicaciones')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    try:
        os.mkdir('Respuestas')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    for i in range(0,len(listaContenido1[0])):

        file_object = open("Publicaciones\\Archivo"+str(i+1)+".txt","w",encoding="utf-8")
        file_object.write(str(listaContenido1[0][i]))
        file_object.write("\n")
        file_object.write(str(listaContenido1[1][i]))
        file_object.write("\n")
        file_object.write(str(listaContenido1[2][i]))
        file_object.write("\n")
        file_object.write(str(listaContenido1[3][i]))
        file_object.write("\n")
        a = listaContenido1[4][i]
        b = str(a)
        file_object.write(str(listaContenido1[5][i]))
        file_object.write("\n")
        file_object.write(b)
        
    for i in range(0,len(listaContenido2[0])):

        file_object = open("Respuestas\\Archivo"+str(i+1)+".txt","w",encoding="utf-8")
        file_object.write(str(listaContenido2[0][i]))
        file_object.write("\n")
        file_object.write(str(listaContenido2[1][i]))
        file_object.write("\n")
        file_object.write(str(listaContenido2[2][i]))
        file_object.write("\n")
        file_object.write(str(listaContenido2[3][i]))
        
crearTxt()