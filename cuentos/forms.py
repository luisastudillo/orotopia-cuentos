from .models import *
from django import forms

class CuentoForm(forms.ModelForm):
	portada = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*'}))
	class Meta:
		model = Cuento
		fields = ('titulo', 'descripcion', 'portada')

class PaginaForm(forms.ModelForm):
	audio = forms.FileField(widget=forms.FileInput(attrs={'accept':'audio/*'}))
	imagen = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*'}))
	class Meta:
		model = Pagina
		fields = ('imagen', 'audio')

class TituloCuentoForm(forms.ModelForm):
	class Meta:
		model = Cuento
		fields = ('titulo',)

class DescripcionCuentoForm(forms.ModelForm):
	class Meta:
		model = Cuento
		fields = ('descripcion',)

class PortadaCuentoForm(forms.ModelForm):
	portada = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*'}))
	class Meta:
		model = Cuento
		fields = ('portada',)

class ImagenPaginaForm(forms.ModelForm):
	imagen = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*'}))
	class Meta:
		model = Pagina
		fields = ('imagen',)

class AudioPaginaForm(forms.ModelForm):
	audio = forms.FileField(widget=forms.FileInput(attrs={'accept':'audio/*'}))
	class Meta:
		model = Pagina
		fields = ('audio',)