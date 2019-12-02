from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    idUsuario = models.CharField(max_length=100, primary_key=True, unique=True)
    edad = models.CharField(max_length=3, null=False)
    GENEROS = (('M', 'Masculino'),('F', 'Femenino'))
    genero = models.CharField(max_length=1, choices=GENEROS)
    ocupacion = models.ForeignKey('Ocupacion', on_delete=models.CASCADE)
    codigoPostal = models.CharField(max_length=10, null=False)
=======
from unittest.util import _MAX_LENGTH

# Create your models here.

class Usuario(models.Model):
    idUsuario= models.CharField(max_length=100,primary_key=True)
    edad=models.IntegerField(null=False)
    sexo=models.CharField(max_length=1,null=False)
    codigoPostal=models.CharField(max_lenght=10)
>>>>>>> a458b39c3855db1513e8681023efea2844d9d5e7
    
    def __str__(self):

        return self.idUsuario
<<<<<<< HEAD

class Ocupacion(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class Pelicula(models.Model):
    idPelicula = models.CharField(max_length=100, primary_key=True, unique=True)
    titulo = models.CharField(max_length=100, blank=False)
    fechaEstreno = models.DateField(auto_now=False, null=False)
    imdbUrl = models.URLField(max_length=200, verify_exists=True)
    categoria = models.ManyToManyField('Categoria')

    def __str__(self):

        return self.idPelicula

class Categoria(models.Model):
    idCategoria = models.CharField(max_length=100, primary_key=True, unique=True)
    nombre = models.CharField(max_length=40, null=False)
=======
    
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
>>>>>>> a458b39c3855db1513e8681023efea2844d9d5e7

    def __str__(self):

        return self.idCategoria
<<<<<<< HEAD



=======
    
class puntuacion(models.Model):
    

    def __str__(self):

        return self.idCategoria
    
>>>>>>> a458b39c3855db1513e8681023efea2844d9d5e7
