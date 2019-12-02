from django.db import models
from unittest.util import _MAX_LENGTH

# Create your models here.

class Usuario(models.Model):
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
    
