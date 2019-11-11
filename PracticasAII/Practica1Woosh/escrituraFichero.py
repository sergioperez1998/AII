from Practica1Woosh import EjercicioWoosh
import pickle
import os

def escrituraFichero():
    
    datos= EjercicioWoosh.obtenerDatos           
         
    titulos=datos(0)
    print(titulos)
    enlaces=datos(1)
    print(enlaces)
    nombres=datos(2)
    print(nombres)
    fechas=datos(3)
    print(fechas)
    numeroRespuestas=datos(4)
    print(numeroRespuestas)
    numeroVisitas=datos(5)
    print(numeroVisitas)
    contadorLinea=0
    
    while contadorLinea < len(titulos):
        
        archivo = open("C:\\Users\\sergi\\Desktop\\Mi Equipo\\Facultad\\CUARTO CURSO\\ACCESO INTELIGENTE A LA INFORMACION\\REPO\\AII\\PracticasAII\\Practica1Woosh\\Temas\\"+str(contadorLinea+1)+".txt","w")
        
        archivo.write(titulos[contadorLinea]+ "\n")
        archivo.write(enlaces[contadorLinea]+"\n")
        archivo.write(nombres[contadorLinea]+"\n")
        archivo.write(fechas[contadorLinea]+"\n")
        archivo.write(numeroRespuestas[contadorLinea]+"\n")
        archivo.write(numeroVisitas[contadorLinea])
        
        
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
        archivo.close()
escrituraFichero()
