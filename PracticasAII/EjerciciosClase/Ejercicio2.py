import urllib.request
import re


response = urllib.request.urlopen('http://www.us.es/rss/feed/portada')
html = response.read().decode('utf-8')
filtro_titulo = re.findall("<title>(.+)</title>",html)
filtro_link = re.findall("<link>(.+)</link>",html)
filtro_fecha= re.findall("<pubDate>(.+)</pubDate>",html)
for titulo in filtro_titulo:
    for link in filtro_link:
        for fecha in filtro_fecha:
            print("Titulo: "+titulo)
            print("Link: "+link)
            print("Fecha: "+fecha)
            print("\n")






