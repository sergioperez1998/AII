from django.contrib import admin
from main.models import Artista, Usuario, UsuarioArtista, Etiqueta,\
    UsuarioEtiquetaArtista

# Register your models here.

admin.site.register(Artista)
admin.site.register(Usuario)
admin.site.register(UsuarioArtista)
admin.site.register(Etiqueta)
admin.site.register(UsuarioEtiquetaArtista)
