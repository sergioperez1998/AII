def __init__(self):
    print (self.e1_a('1234567'))
    print (self.e1_b('mi archivo de texto.txt'))

    
def e1_a(s):
    return ",".join(list(s))

def e1_b(s):
    return s.replace(' ','_')

def e1_c(self, s, a):
    return s + a.replace(a, "XXXX")

def e1_d(self, s):
    a = list(s)
    b = []
    c = ""
    i = 0
    for x in a:
        b.append(x)
        i=i+1
        if i == 3:
            b.append(".")
            i=0
    
    for h in b:
        c = c + h
    return c

def e2_a(self,a,b):
    if a in b:
        return a in b 
    if b in a:
        return b in a

def e2_b(self, a,b):
    return a if a.lower() < b.lower() else b
    
def tuplasListas_a(self, a):
    
    b=0
    c=[]
    for i in a:
        c.append("Estimado " + a[b] + " vote por mi.")
        b = b+1
    return c

def tuplasListas_b(self,t,p,n):
        t1 = t[p:p+n]
        return tuplasListas_a(self=None,a=t1)    
    
    
def agendaSimplificada(self, a, b):
    
    res = []
    for x in b:
        if a in x[0]:
            res.append("Nombre: "+ x[0]+ ", Telefono: "+ str(x[1]))
            return res

def rellenoAgenda(self):
    
    res={}
    i=0
    while i == 0: 
        print("Ingrese un nombre:")
        nombre=input()
        print("Ingrese un numero de telefono:")
        telefono=input()
        res.setdefault(nombre, int(telefono))
        print("Seguimos anadiendo contactos: Si/No")
        seguir=input()
        if seguir in "No":
            i=1
    return res    

def busquedaAgenda(self,a):
    
    agenda=rellenoAgenda(self=None)
    i=0
    print(agenda)
    while i==0:
        for x in agenda.keys():
            if a in x:
                telefono = agenda[x]
                print("El numero de telefono de "+ a+" es:",telefono)
                print("Cambiar el numero de telefono Si/No")
                cambiar = input()
                if cambiar in "Si":
                    print("Nuevo numero de telefono:")
                    telefono=input()
                    print("Telefono cambiado a:" ,telefono)
                    agenda[x]= int(telefono)
        print("Anadir nuevo contacto: Si/No")
        anadir=input()
        if anadir in "Si":
            print("Nombre:")
            nombre=input()
            print("Telefono:")
            telefono =input()
            agenda.setdefault(nombre, int(telefono))
        print("Para salir del sistema presionar *")
        salir=input()
        if salir in "*":
            i=1
    return agenda


print(e1_a(s='1234567'))
print(e1_b(s='mi archivo de texto.txt'))
print(e1_c(self=None, s= "su clave es:", a="1540"))
print(e1_d(self =None, s="2552552550"))   
print(e2_a(self=None, a = "cadena", b = "subcadena"))
print(e2_b(self= None, a = "gnomo", b = "kdg"))
print(tuplasListas_a(self= None, a =("Elias","Chamorro")))
print(tuplasListas_b(self=None,t=('Luis','Marta','Paula','Luis'),p=1,n=2))
print(agendaSimplificada(self=None, a="Sergio_Perez_Martin", b=[("Sergio_Perez_Martin", 955901598),("Jesus Elias Rodriguez", 95621585)]))
print(rellenoAgenda(self=None))
print(busquedaAgenda(self=None, a = "Sergio")) 


class Corcho:
    
    def __init__(self,Nombre):
        self.bodega=Nombre

class Botella:
    
    def __init__(self,Corcho):
        self.corcho = Corcho
        print("Botella de la bodega "+ Corcho.bodega)
        
class Sacacorcho:
    
    def __init__(self):
        self.corcho = None
        
    def descolchar(self,botella):
        print("Descolchar una botella")
        self.corcho=botella.corcho
        botella.corcho = None

class Personaje:
    
    def __init__(self,Nombre,Vida,PuntosDeMovimiento):
        self.nombre = Nombre
        self.vida = Vida
        self.velocidad = PuntosDeMovimiento
        self.posicion = {"Norte":0, "Sur":0, "Este":0, "Oeste":0}
        
    def recibirAtaque(self, fuerza):
        self.vida = self.vida - fuerza
        if self.vida <0:
            print("Has muerto, te has quedado sin PV")
        else:
            print("Te quedan "+self.vida+" PV")
            
    def mover(self,direccion):
        self.posicion[direccion] = self[direccion]+self.velocidad
        
class Soldado:
    
    def __init__(self,Fuerza):
        Personaje.__init__(self=None, "Sergio", 1000, 10)
        self.fuerza = Fuerza
    
    def Atacar(self,personaje):
        personaje.recibirAtaque(self.fuerza)
        
class Campesino:
    
    def __init__(self,Cosecha):
        Personaje.__init__(self=None, "Jesus", 500, 15)
        self.cosecha = Cosecha
        
    def Cosechar(self):
        return self.cosecha
    
class Herencia:
    
    def __init__(self):
        soldado = Soldado()
        campesino = Campesino()
        soldado.Atacar(campesino)
        print (campesino.cosecha)
        
         



