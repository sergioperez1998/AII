#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Receta(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    ingredientes = models.TextField(help_text='Redacta los ingredientes')
    prepacion = models.TextField(verbose_name='Preparacion')
    imagen = models.ImageField(upload_to='recetas', verbose_name='Imagen')
    tiempo_registro = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo
    
class Pelicula(models.Model):
    titulo = models.CharField(max_length=100, unique=True, null=False)
    año= models.IntegerField(null=False)
    resumen = models.TextField(help_text='Redacta un resumen sobre la pelicula',null=False)
    categoria = models.TextField(help_text='Seleccione una categoria',null=False)
    director = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return self.titulo
