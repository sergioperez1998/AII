from django.db import models

# Create your models here.
class Artista(models.Model):
    idArtista=models.TextField(primary_key=True)
    name=models.TextField(verbose_name='Nombre', unique=True)
    url=models.URLField(verbose_name = 'Url del artista')
    pictureUrl=models.URLField(verbose_name = 'Url de la imagen')
   
    def __str__(self):
        return self.name
