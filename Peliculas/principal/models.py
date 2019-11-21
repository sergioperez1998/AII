#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    fechaNacimiento = models.DateField(auto_now=False, null=False)
    categoriaPreferida=models.TextField(help_text='Categoria Pelicula',null=False)
    usuario = models.OneToOneField(parent_link=User,on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.categoriaPreferida
    

    

class Director(models.Model):
    biografia=models.TextField(help_text='biogradia',null=False)
    peliculasDirigidas=models.TextField(help_text='escribir peliculas separadas por comas ',null=False)
    usuario = models.OneToOneField(parent_link=User,on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.categoriaPreferida