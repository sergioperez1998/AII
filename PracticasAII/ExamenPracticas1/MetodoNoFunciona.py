encoding = "utf-8"
from bs4 import BeautifulSoup
import urllib.request as urllib2

def obtencionDatos():
        
        url = "https://www.sprinter.es/zapatillas-hombre"
        url2="https://www.sprinter.es/zapatillas-de-hombre?page=2&per_page=20"
        response = urllib2.urlopen(url)
        webContent = response.read()
        soup = BeautifulSoup(webContent, 'html.parser')
        
        listaNombres=[]
        listaMarcas=[]
        listaPrecios=[]
        listaPreciosAntiguo=[]
        listaEstrellas=[]
        listaPuntuaciones=[]
        
        for datosProducto in soup.findAll("div", attrs={"class":"product__data"}):
            listaNombres.append(datosProducto.a.string)
            listaMarcas.append(datosProducto.a.string.split(" ")[0])
            for precio in datosProducto.findAll("span", attrs={"class":"product__price--actual"}):
                listaPrecios.append(precio.string.split(" ")[0])
            for precios in datosProducto.findAll("div", attrs={"class":"product__price"}):
                blanco = precios.span.next_sibling.string
                if  "Comment" in type(blanco).__name__ :
                    listaPreciosAntiguo.append(None)
                else: 
                    listaPreciosAntiguo.append(blanco.split(" ")[0])
                    
            url_elementos= "https://www.sprinter.es" + datosProducto.a.get("href")
            response = urllib2.urlopen(url_elementos)
            webContent2 = response.read()
            soup2 = BeautifulSoup(webContent2, 'html.parser')
            dots = dots = soup2.find("div",class_="average")
            ratio = dots.span.string
            print(ratio)
            
            
        
print(obtencionDatos())