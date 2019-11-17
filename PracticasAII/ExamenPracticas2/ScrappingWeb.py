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
    
    i=1
    lista=[]
    
    while i<4:
        url="http://www.sensacine.com/noticias/?page="+str(i)
        if i == 1:
            lista=obtenerDatos(url)
        else:
            lista[0].extend(obtenerDatos(url)[0])
            lista[1].extend(obtenerDatos(url)[1])
            lista[2].extend(obtenerDatos(url)[2])
            lista[3].extend(obtenerDatos(url)[3])
            lista[4].extend(obtenerDatos(url)[4])
        i=i+1
     
    return lista

def obtenerDatos(url):
    
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read().decode("latin-1"), 'lxml')
    
    
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
        a = lista[4][i]
        b = str(a)
        file_object.write(b)