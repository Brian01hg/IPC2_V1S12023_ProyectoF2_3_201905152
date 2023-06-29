from django import forms
from .models import Sala, Tarjeta

class PeliculaForm(forms.Form):
    titulo = forms.CharField(label='Título')
    director = forms.CharField(label='Director')
    anio = forms.IntegerField(label='Año')
    fecha = forms.DateField(label='Fecha')
    hora = forms.TimeField(label='Hora')
    imagen = forms.URLField(label='URL de la imagen')
    precio = forms.DecimalField(label='Precio')

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['numero', 'asientos']

class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ['tipo', 'numero', 'titular', 'fecha_expiracion']

