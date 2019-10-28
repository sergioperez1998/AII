import urllib.request
from bs4 import BeautifulSoup
import re

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
    #return listado_title,listado_link,listado_fecha
    return muestraDatos(listado_title, listado_link, listado_fecha)  

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
        
def muestraDatos(l1,l2,l3):
    
    i=0
    while i < len(l1):
        print("Titulo: "+ str(l1[i]))
        print("Link: "+ str(l2[i]))
        print("Fecha: "+ str(l3[i]))
        print("\n")
        i=i+1

print(obtencionNoticias())    
    



