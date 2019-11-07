from Practica1Woosh import EjercicioWoosh
import pickle
import os

def escrituraFichero():
    
    datos= EjercicioWoosh.obtenerDatos()
    
    for contenidoDatos in datos:
        
        i=1
        archivo = open("Desktop/hola.txt","w")
        #archivo = open("Desktop\\"+str(i)+".txt","r+")
        #archivo = open("Temas\\"+str(i)+".txt","r+")
        titulos=contenidoDatos[0]
        enlaces=contenidoDatos[1]
        nombres=contenidoDatos[2]
        fechas=contenidoDatos[3]
        numeroRespuestas=contenidoDatos[4]
        numeroVisitas=contenidoDatos[5]
        contadorLinea=0
        while contadorLinea < len(titulos):
            
            archivo.write(titulos[contadorLinea]+ os.linesep)
            archivo.write(enlaces[contadorLinea]+os.linesep)
            archivo.write(nombres[contadorLinea]+os.linesep)
            archivo.write(fechas[contadorLinea]+os.linesep)
            archivo.write(numeroRespuestas[contadorLinea]+os.linesep)
            archivo.write(numeroVisitas[contadorLinea]+os.linesep)
            archivo.close()
            
            '''
            archivo.write(titulos[contadorLinea]+"\n")
            archivo.write(enlaces[contadorLinea]+"\n")
            archivo.write(nombres[contadorLinea]+"\n")
            archivo.write(fechas[contadorLinea]+"\n")
            archivo.write(numeroRespuestas[contadorLinea]+"\n")
            archivo.write(numeroVisitas[contadorLinea]+"\n")
            '''
            '''
            pickle.dump(titulos[contadorLinea]+"\n",archivo)
            pickle.dump(enlaces[contadorLinea]+"\n",archivo)
            pickle.dump(nombres[contadorLinea]+"\n",archivo)
            pickle.dump(fechas[contadorLinea]+"\n",archivo)
            pickle.dump(numeroRespuestas[contadorLinea]+"\n",archivo)
            pickle.dump(numeroVisitas[contadorLinea]+"\n",archivo)
            '''
            contadorLinea=contadorLinea+1
        
        i=i+1