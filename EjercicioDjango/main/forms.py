#encoding:utf-8
from django import forms
   
class EventosBusquedaIdiomasForm(forms.Form):
    idUsuario = forms.CharField(label="Idioma del evento", widget=forms.TextInput, required=True)
    
class EventosBusquedaFechaForm(forms.Form):
    fecha = forms.IntegerField(label="fecha del evento", widget=forms.TextInput, required=True)