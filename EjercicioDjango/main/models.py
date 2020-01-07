#encoding:utf-8

from django.db import models

class Municipio(models.Model):
    nombre = models.TextField(verbose_name='Municipio', unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )

class Tipo(models.Model):
    nombre = models.TextField(verbose_name='Tipo')

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering =('nombre', )

class Lenguaje(models.Model):
    nombre = models.TextField(verbose_name='Lenguaje', primary_key = True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering =('nombre', )

class Evento(models.Model):
    nombre = models.TextField(verbose_name='Nombre', help_text='Debe introducir un nombre')
    fechaInicio = models.DateField(verbose_name='Fecha Inicio', null=True)
    fechaFin = models.DateField(verbose_name='Fecha Fin', null=True)
    precio = models.TextField(verbose_name='Precio', help_text='Debe introducir un precio, o gratis')
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    lenguaje = models.ManyToManyField(Lenguaje)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )