from django.contrib import admin
from main.models import Libro, Usuario, Puntuacion

# Register your models here.
admin.site.register(Libro)
admin.site.register(Usuario)
admin.site.register(Puntuacion)
