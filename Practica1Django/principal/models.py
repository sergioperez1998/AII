from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    
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
    
    