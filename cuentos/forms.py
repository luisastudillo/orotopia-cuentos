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

class BannerConfigForm(forms.ModelForm):
	banner = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*'}))
	class Meta:
		model = Config
		fields = ('banner',)

class TramaConfigForm(forms.ModelForm):
	trama = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*'}))
	class Meta:
		model = Config
		fields = ('trama',)

class ColaboradorForm(forms.ModelForm):
	logo = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*'}))
	class Meta:
		model = Colaborador
		fields = ('logo', 'linea1', 'linea2')

class LogoColaboradorForm(forms.ModelForm):
	logo = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*'}))
	class Meta:
		model = Colaborador
		fields = ('logo',)

class Linea1ColaboradorForm(forms.ModelForm):
	class Meta:
		model = Colaborador
		fields = ('linea1',)

class Linea1ColaboradorForm(forms.ModelForm):
	class Meta:
		model = Colaborador
		fields = ('linea2',)