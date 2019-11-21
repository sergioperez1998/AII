from tkinter import *
from tkinter import messagebox

def ventanaPrincipal():
    top = Tk()

    almacenarDatos = Button(top, text="Datos", command = lambda: apartado_a(dirdocs,dirindex))
    almacenarDatos.pack(side = LEFT)

    buscarOfertas = Button(top, text="Buscar", command = ventanaBuscar)
    buscarOfertas.pack(side = RIGHT)

    top.mainloop()

def ventanaDatos():
    dirdocs="Documentos\\"
    dirindex="Index"
    top = Tk()
    indexar = Button(top, text="Cargar", command = ventanaBuscar)
    indexar.pack(side = LEFT)
    salir = Button(top, text= "Salir", command = quit)
    salir.pack(side = RIGHT)
    top.mainloop()

def ventanaBuscar():
    top = Tk()
    dirindex="Index"

    Buscar = Button(top, text="Contenido y Titulo ", command = lambda: apartado_b_a(dirindex))
    Buscar.pack(side = LEFT)

    fecha = Button(top, text="Fecha", command = lambda: apartado_b_b(dirindex))
    fecha.pack(side = LEFT)
    Buscar = Button(top, text="Titulo y fecha ", command = lambda: apartado_b_c(dirindex))
    Buscar.pack(side = RIGHT)


    top.mainloop()

def apartado_b_a(dirindex):
    def mostrar_lista(event):
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            query = QueryParser("titulo", ix.schema ).parse(str(en.get())) | QueryParser("descripcion", ix.schema ).parse(str(en.get()))
            results = searcher.search(query)
            imprimir_b_a(results)
    
    v = Toplevel()
    v.title("Busqueda por contenido y titulo")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una consulta:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)

def imprimir_b_a(results):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for r in results:
        lb.insert(END,r['titutlo'])
        lb.insert(END,r['fecha'])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview) 

def apartado_b_b(dirindex):
    def buscarNoticiasFecha(event):
        
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            try:
                fecha = str(en.get())
                fecha1 = fecha.split("-")[0]
                fecha1Consulta = fecha1.split("/")[2]+fecha1.split("/")[1]+fecha1.split("/")[0] 
                fecha2 = fecha.split("-")[1]
                fecha2Consulta = fecha2.split("/")[2]+fecha2.split("/")[1]+fecha2.split("/")[0] 
                myquery='['+ fecha1Consulta + ' to ' +fecha2Consulta+']'
                print(myquery)
                query = QueryParser("fecha", ix.schema).parse(myquery)
           
                results = searcher.search(query)
                imprimir_b_b(results)
            except:
                print ("Error: Formato de fecha incorrecto")
                
    
    v = Toplevel()
    v.title("Busqueda por fecha ")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una fecha, siguiendo el patron (DD/MM/AAAA [Dia, Tarde]):")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", buscarNoticiasFecha)
    en.pack(side=LEFT)
    
  
def imprimir_b_b(results):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for r in results:
        lb.insert(END,r['titulo'])
        lb.insert(END,r['fecha'])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)

def apartado_b_c(dirindex):
    def mostrar_lista(event):
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            try:
                fecha = str(en2.get())
                titulo = str(en1.get()) 
                mparser = MultifieldParser([fecha, titulo], schema=ix.schema)
           
                results = searcher.search(mparser)
                imprimir_b_b(results)
            except:
                print ("Error: Formato de fecha incorrecto")


    v = Toplevel()
    v.title("Busqueda por titulo y fecha")
    f1 =Frame(v)
    f1.pack(side=TOP)
    l1 = Label(f1, text="Introduzca un titulo :")
    l1.pack(side=LEFT)
    en1 = Entry(f1)
    en1.bind("<Return>", mostrar_lista)
    en1.pack(side=LEFT)
    f2 =Frame(v)
    f2.pack(side=TOP)
    l2 = Label(f2, text="Introduzca una fecha siguiendo el patron (AAAAMMDD) :")
    l2.pack(side=LEFT)
    en2 = Entry(f2)
    en2.bind("<Return>", mostrar_lista)
    en2.pack(side=LEFT)
      
def imprimir_b_c(results):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for r in results:
        lb.insert(END,r['titulo'])
        lb.insert(END,r['fecha'])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview) 

if __name__ == '__main__':
    ventanaPrincipal()