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

def eliminadorDiacriticos(cadena):
    
    s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
    normalize("NFD", cadena), 0, re.I)
    s = normalize('NFC', s)
    return s


def llamadaObtencionDatos():
    
    i=0
    lista=[]
    pagina=9
    
    while i<2:
        url="https://www.sevilla.org/actualidad/noticias?b_start:int=" + str(i*pagina)
        if i == 0:
            lista=obtenerDatos(url)
        else:
            lista[0].extend(obtenerDatos(url)[0])
            lista[1].extend(obtenerDatos(url)[1])
            lista[2].extend(obtenerDatos(url)[2])
            lista[3].extend(obtenerDatos(url)[3])
        i=i+1
     
    return lista

def obtenerDatos(url):
    
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read().decode("utf-8"), 'html.parser')
    
    listaTitulo=[]
    listaFecha=[]
    listaEnlace=[]
    listaTexto=[]
    
    for noticia in soup.findAll("a",attrs={"class":"text-darker"}):
        tituloSinParsear=noticia.find("h2").string.strip()
        tituloParseado= eliminadorDiacriticos(tituloSinParsear)
        listaTitulo.append(tituloParseado)
        fechaSinParsear=(noticia.find("p").string.strip().split(" "))
        listaFecha.append(fechaSinParsear[0]+" "+fechaSinParsear[2])
        enlaceSinParsear=noticia.get("href")
        enlaceParseado= eliminadorDiacriticos(enlaceSinParsear)
        listaEnlace.append(enlaceParseado)
        for texto in noticia.findAll("p",attrs={"class":"newsItem__desc"}):
            textoSinParsear=texto.string.strip()
            textoParseado= eliminadorDiacriticos(textoSinParsear)
            listaTexto.append(textoParseado)
    
    return listaTitulo, listaFecha, listaEnlace, listaTexto

def crearTxt():
        
    lista = llamadaObtencionDatos()
    
    try:
        os.mkdir('Documentos')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    for i in range(0,len(lista[0])):

        file_object = open("Documentos\\Archivo"+str(i+1)+".txt","w",encoding="utf-8")
        file_object.write(str(lista[0][i]))
        file_object.write("\n")
        file_object.write(str(lista[1][i]))
        file_object.write("\n")
        file_object.write(str(lista[2][i]))
        file_object.write("\n")
        file_object.write(str(lista[3][i]))
        file_object.write("\n")

crearTxt()