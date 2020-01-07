<<<<<<< HEAD
from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
=======
from unittest.util import _MAX_LENGTH
>>>>>>> a458b39c3855db1513e8681023efea2844d9d5e7

# Create your models here.

class Usuario(models.Model):
<<<<<<< HEAD
    
    idUsuario = models.IntegerField(primary_key=True, null=False)
    edad = models.IntegerField(null = False)
    sexo = models.CharField(max_length=1,null=False)
    codigoPostal=models.IntegerField(null = False)
        
    def __str__(self):
        idUsuarioString=self.idUsuario
        return str(idUsuarioString)
    
class Pelicula (models.Model):
    
    idPelicula = models.IntegerField(primary_key=True, null=False)
    titulo = models.CharField(null = False)
    fechaEstreno = models.DateField(null=False)
    imdbUrl= models.URLField(null = False)
    categorias = models.ManyToManyField("Categoria")
    puntuaciones = models.ManyToManyField("Puntuacion")
    
    def __str__(self):
        idPeliculaString=self.idPelicula
        return str(idPeliculaString)
    
class Categoria (models.Model):
    
    IdCategoria = models.IntegerField(primary_key=True, null = False)
    nombre = models.CharField(null = False)
    
    def __str__(self):
        idCategoriaString=self.IdCategoria
        return str(idCategoriaString)
    
class Ocupacion (models.Model):
    
    nombre = models.CharField(primary_key = True, null = False)
    usuarios= models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
class Puntuacion(models.Model):
    
    puntuacion= models.IntegerField(primary_key = True, null = False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    
    
=======
    idUsuario= models.CharField(max_length=100,primary_key=True)
    edad=models.IntegerField(null=False)
    sexo=models.CharField(max_length=1,null=False)
    codigoPostal=models.CharField(max_lenght=10)
    
    def __str__(self):

        return self.idUsuario
    
class ocupacion(models.Model):
    nombre=models.CharField(max_length=100)
    usuarios=models.ForeignKey(Usuario,on_delete=models.CASCADE)

    def __str__(self):

        return self.name
    
class Pelicula(models.Model):
    idPelicula= models.CharField(max_length=100,primary_key=True)
    titulo = models.CharField(max_length=100, unique=True, null=False)
    fechaEstreno= models.DateField(null=False)
    imdbUrl=models.URLField(verify_exists=True, max_length=200)
    
    
    def __str__(self):
        return self.idPelicula
    
class categoria(models.Model):
    idCategoria= models.CharField(max_length=100,primary_key=True)
    nombre=models.CharField(max_length=100)
    usuarios=models.ManyToManyField(Pelicula)

    def __str__(self):

        return self.idCategoria
    
class puntuacion(models.Model):
    

    def __str__(self):

        return self.idCategoria
    
>>>>>>> a458b39c3855db1513e8681023efea2844d9d5e7
=======
>>>>>>> a2c032a6f58d0c862c39762df15cabe0e0a37b1a
