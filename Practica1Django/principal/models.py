from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    idUsuario = models.CharField(max_length=100, primary_key=True, unique=True)
    edad = models.CharField(max_length=3, null=False)
    GENEROS = (('M', 'Masculino'),('F', 'Femenino'))
    genero = models.CharField(max_length=1, choices=GENEROS)
    ocupacion = models.ForeignKey('Ocupacion', on_delete=models.CASCADE)
    codigoPostal = models.CharField(max_length=10, null=False)
    
    def __str__(self):

        return self.idUsuario

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

    def __str__(self):

        return self.idCategoria



