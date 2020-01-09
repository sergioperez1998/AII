#encoding:utf-8
from django.db import models

# Create your models here.
class Artista(models.Model):
    idArtista=models.TextField(primary_key=True)
    name=models.TextField(verbose_name='Nombre', unique=True)
    url=models.URLField(verbose_name = 'Url del artista')
    pictureUrl=models.URLField(verbose_name = 'Url de la imagen',null=True)
   
    def __str__(self):
        return self.name
        
class Etiqueta(models.Model):
    
    id=models.TextField(primary_key=True)
    tagValue=models.TextField(verbose_name='Valor de la tag', unique=True)
    def __str__(self):
        return self.tagValue

class Usuario(models.Model):
    idUsuario=models.TextField(primary_key=True)
    def __str__(self):
        return self.idUsuario
        
class UsuarioArtista(models.Model):
    
    idUsuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idArtista=models.ForeignKey(Artista, on_delete=models.CASCADE)
    tiempoEscucha=models.IntegerField()
    def __str__(self):
        return self.tiempoEscucha

class UsuarioEtiquetaArtista(models.Model):
    
    idUsuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idArtista=models.ForeignKey(Artista, on_delete=models.CASCADE)
    idTag=models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    fecha=models.DateField(null=False, blank=False)
    def __str__(self):
        return self.fecha


        
    
    