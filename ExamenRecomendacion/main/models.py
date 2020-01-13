from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

class Libro(models.Model):
    bookId=models.AutoField(primary_key=True)
    titulo=models.TextField(verbose_name='Titulo',unique=True)
    autor=models.TextField(verbose_name='Autor')
    genero=models.TextField(verbose_name='Genero')
    idioma=models.TextField(verbose_name='Idioma')
    puntuaciones= models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return self.titulo
    
class Usuario(models.Model):
    idUsuario=models.TextField(primary_key=True)
    def __str__(self):
        return str(self.idUsuario)
    
class Puntuacion(models.Model):
    IdUsuario=models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    bookId=models.ForeignKey(Libro, on_delete=models.CASCADE, null=True)
    puntuacion= models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    def __str__(self):
        return str(self.puntuacion)
    

