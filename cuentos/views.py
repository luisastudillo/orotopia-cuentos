from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import redirect
import os

global rutaeliminar
global rutaeliminar1
global rutaeliminar2
global rutaeliminar3

# Create your views here.

def redirectListaCuentos(request):
	return redirect('listaCuentos', permanent=False)

def listaCuentos(request):
	listacuentos = Cuento.objects.all()
	listacolabs = Colaborador.objects.all()
	config = Config.objects.all().first()
	
	return render(request, 'cuentos/cuentosindex.html', {'listacuentos': listacuentos, 'listacolabs': listacolabs, 'config':config})

def verCuento(request, cuentoid):
	lista = Pagina.objects.filter(cuento=cuentoid)
	cuento = Cuento.objects.get(id=cuentoid)

	return render(request, 'cuentos/cuento.html', {'lista': lista, 'cuento': cuento})

def agregarCuento(request):
	if request.user.is_authenticated:
		agregado=False
		error=False
		if request.method == "POST":
			form = CuentoForm(request.POST, request.FILES)
			if form.is_valid():
				cuento = form.save()
				agregado=True
				return redirect('agregarpagina', cuento.id)
			else:
				error=True
		form = CuentoForm()
		return render(request, 'cuentos/agregarcuento.html', {'form': form,'error': error,'agregado': agregado})
	else:
		return redirect('listaCuentos', permanent=False)

def agregarPagina(request, cuentoid):
	if request.user.is_authenticated:
		agregado=False
		error=False
		cuento = Cuento.objects.get(id=cuentoid)
		siguiente = cuento.n_paginas + 1
		if request.method == "POST":
			siguiente = siguiente + 1
			form = PaginaForm(request.POST, request.FILES)
			if form.is_valid():
				pagina = form.save(commit=False)
				pagina.cuento=cuento
				pagina.numerar()
				pagina.save()
				pagina.dividir()
				pagina.save()
				agregado=True
			else:
				error=True
		form = PaginaForm()
		return render(request, 'cuentos/agregarpagina.html', {'form':form,'error':error,'agregado':agregado, 'cuento':cuento, 'siguiente':siguiente})
	else:
		return redirect('listaCuentos', permanent=False)

def editarTituloCuento(request, cuentoid):
	if request.user.is_staff:
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			form=TituloCuentoForm(request.POST,instance=cuento)
			if form.is_valid():
				form.save()
				mensaje = "Cambios guardados"
				return redirect('listaPaginas', cuentoid)
		else:
			form=TituloCuentoForm(instance=cuento)
			titulo=cuento.titulo
			template = 'cuentos/editartitulocuento.html'
			book = {'form':form, 'titulo':titulo, 'cuento':cuento}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def editarDescripcionCuento(request, cuentoid):
	if request.user.is_staff:
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			form=DescripcionCuentoForm(request.POST,instance=cuento)
			if form.is_valid():
				form.save()
				mensaje = "Cambios guardados"
				return redirect('listaPaginas', cuentoid)
		else:
			form=DescripcionCuentoForm(instance=cuento)
			titulo=cuento.titulo
			template = 'cuentos/editardescripcioncuento.html'
			book = {'form':form, 'titulo':titulo, 'cuento':cuento}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def editarPortadaCuento(request, cuentoid):
	if request.user.is_staff:
		global rutaeliminar
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			form=PortadaCuentoForm(request.POST,request.FILES,instance=cuento)
			if form.is_valid():
				form.save()
				print("Anterior " + os.path.basename(rutaeliminar))
				print("Nueva " + os.path.basename(cuento.portada.path))
				os.remove(rutaeliminar)
				mensaje = "Cambios guardados"
				return redirect('listaPaginas', cuentoid)
		else:
			rutaeliminar = cuento.portada.path
			print("Se va a eliminar " + os.path.basename(rutaeliminar))
			form=PortadaCuentoForm(instance=cuento)
			titulo=cuento.titulo
			template = 'cuentos/editarportadacuento.html'
			book = {'form':form, 'titulo':titulo, 'cuento':cuento}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def editarImagenPagina(request, cuentoid, paginaid):
	if request.user.is_staff:
		global rutaeliminar
		global rutaeliminar1
		global rutaeliminar2
		pagina = Pagina.objects.get(id=paginaid)
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			form=ImagenPaginaForm(request.POST, request.FILES, instance=pagina)
			if form.is_valid():
				try:
					form.save()
					pagina.dividir()
					pagina.save()
					os.remove(rutaeliminar)
					print("Imagen borrada " + os.path.basename(rutaeliminar))
					os.remove(rutaeliminar1)
					print("Imagen1 borrada " + os.path.basename(rutaeliminar1))
					os.remove(rutaeliminar2 )
					print("Imagen2 borrada " + os.path.basename(rutaeliminar2))
				except Exception as e:
					print(e)
					return redirect('errorEliminarPagina', cuentoid, permanent=False)
				mensaje = "Cambios guardados"
				return redirect('listaPaginas', cuentoid)
			else:
				print("mal mal")
		else:
			rutaeliminar = pagina.imagen.path
			rutaeliminar1 = pagina.imagen1.path
			rutaeliminar2 = pagina.imagen2.path
			form=ImagenPaginaForm(instance=pagina)
			numero = pagina.numero
			template = 'cuentos/cambiarimagenpagina.html'
			book = {'form':form, 'cuento':cuento, 'numero':numero}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def editarAudioPagina(request, cuentoid, paginaid):
	if request.user.is_staff:
		global rutaeliminar
		pagina = Pagina.objects.get(id=paginaid)
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			form=AudioPaginaForm(request.POST, request.FILES, instance=pagina)
			if form.is_valid():
				form.save()
				os.remove(rutaeliminar)
				mensaje = "Cambios guardados"
				return redirect('listaPaginas', cuentoid)
			else:
				print("mal mal")
		else:
			rutaeliminar = pagina.audio.path
			form=AudioPaginaForm(instance=pagina)
			template = 'cuentos/cambiaraudiopagina.html'
			book = {'form':form, 'cuento':cuento, 'pagina':pagina}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def eliminarCuento(request, cuentoid):
	if request.user.is_staff:
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			lista = Pagina.objects.filter(cuento=cuentoid)
			for pagina in lista:
				ruta = pagina.imagen.path
				ruta1 = pagina.imagen1.path
				ruta2 = pagina.imagen2.path
				ruta3 = pagina.audio.path
				pagina.delete()
				os.remove(ruta)
				os.remove(ruta1)
				os.remove(ruta2)
				os.remove(ruta3)
			cuento.delete()
			mensaje = "Cuento eliminado"
			return redirect('listaCuentos', permanent=False)
		else:
			template = 'cuentos/eliminarcuento.html'
			book = {'cuento':cuento}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def eliminarPagina(request, cuentoid, paginaid):
	if request.user.is_staff:
		global rutaeliminar
		global rutaeliminar1
		global rutaeliminar2
		global rutaeliminar3
		cuento = Cuento.objects.get(id=cuentoid)
		pagina = Pagina.objects.get(id=paginaid)
		if request.POST:
			try:
				os.remove(rutaeliminar)
				os.remove(rutaeliminar1)
				os.remove(rutaeliminar2)
				os.remove(rutaeliminar3)
				pagina.delete()
				lista = Pagina.objects.filter(cuento=cuentoid)
				num=0
				for pagina in lista:
					num=num+1
					pagina.numero=num
					pagina.save()
				cuento.n_paginas=num
				cuento.save()
				return redirect('listaPaginas', cuentoid,  permanent=False)
			except Exception as e:
				print(e)
				return redirect('errorEliminarPagina', cuentoid, permanent=False)
			
		else:
			rutaeliminar = pagina.imagen.path
			rutaeliminar1 = pagina.imagen1.path
			rutaeliminar2 = pagina.imagen2.path
			rutaeliminar3 = pagina.audio.path
			template = 'cuentos/eliminarpagina.html'
			book = {'cuento':cuento, 'pagina':pagina}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def errorEliminarPagina(request, cuentoid):
	cuento = Cuento.objects.get(id=cuentoid)
	return render(request, 'cuentos/erroreliminarpagina.html', {'cuento':cuento})

def listaPaginas(request, cuentoid):
	lista = Pagina.objects.filter(cuento=cuentoid)
	cuento = Cuento.objects.get(id=cuentoid)
	return render(request, 'cuentos/listapaginas.html', {'lista': lista, 'cuento':cuento})

def config(request):
	lista = Colaborador.objects.all()
	config = Config.objects.all().first()
	return render(request, 'cuentos/config.html', {'lista': lista, 'config':config})

def bannerConfig(request):
	if request.user.is_staff:
		global rutaeliminar
		config = Config.objects.all().first()
		if request.POST:
			form=BannerConfigForm(request.POST, request.FILES, instance=config)
			if form.is_valid():
				form.save()
				config.save()
				print("Actual: " + config.banner.path)
				print("Anterior: " + rutaeliminar)
				os.remove(rutaeliminar)
				mensaje = "Cambios guardados"
				return redirect('config')
			else:
				print("mal mal")
		else:
			rutaeliminar = config.banner.path
			print("Grabada anterior: " + rutaeliminar)
			form=BannerConfigForm(instance=config)
			template = 'cuentos/bannerconfig.html'
			book = {'form':form, 'config':config}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def tramaConfig(request):
	if request.user.is_staff:
		global rutaeliminar
		config = Config.objects.all().first()
		if request.POST:
			form=TramaConfigForm(request.POST, request.FILES, instance=config)
			if form.is_valid():
				form.save()
				config.save()
				os.remove(rutaeliminar)
				mensaje = "Cambios guardados"
				return redirect('config')
			else:
				print("mal mal")
		else:
			rutaeliminar = config.trama.path
			form=TramaConfigForm(instance=config)
			template = 'cuentos/tramaconfig.html'
			book = {'form':form, 'config':config}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def colaboradorLogo(request, colaboradorid):
	if request.user.is_staff:
		global rutaeliminar
		colaborador = Colaborador.objects.get(id=colaboradorid)
		if request.POST:
			form=LogoColaboradorForm(request.POST, request.FILES, instance=colaborador)
			if form.is_valid():
				form.save()
				os.remove(rutaeliminar)
				mensaje = "Cambios guardados"
				return redirect('config')
			else:
				print("mal mal")
		else:
			rutaeliminar = colaborador.logo.path
			form=LogoColaboradorForm(instance=colaborador)
			template = 'cuentos/logocolaborador.html'
			book = {'form':form, 'colaborador':colaborador}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def colaboradorLinea1(request, colaboradorid):
	if request.user.is_staff:
		colaborador = Colaborador.objects.get(id=colaboradorid)
		if request.POST:
			form=Linea1ColaboradorForm(request.POST, instance=colaborador)
			if form.is_valid():
				form.save()
				mensaje = "Cambios guardados"
				return redirect('config')
			else:
				print("mal mal")
		else:
			form=Linea1ColaboradorForm(instance=colaborador)
			titulo=colaborador.linea1 + " " + colaborador.linea2
			template = 'cuentos/linea1colaborador.html'
			book = {'form':form, 'colaborador':colaborador, 'titulo':titulo}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def colaboradorLinea2(request, colaboradorid):
	if request.user.is_staff:
		colaborador = Colaborador.objects.get(id=colaboradorid)
		if request.POST:
			form=Linea1ColaboradorForm(request.POST, instance=colaborador)
			if form.is_valid():
				form.save()
				mensaje = "Cambios guardados"
				return redirect('config')
			else:
				print("mal mal")
		else:
			form=Linea1ColaboradorForm(instance=colaborador)
			titulo=colaborador.linea1 + " " + colaborador.linea2
			template = 'cuentos/linea2colaborador.html'
			book = {'form':form, 'colaborador':colaborador, 'titulo':titulo}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def colaboradorEliminar(request, colaboradorid):
	if request.user.is_staff:
		global rutaeliminar
		colaborador = Colaborador.objects.get(id=colaboradorid)
		if request.POST:
			colaborador.delete()
			os.remove(rutaeliminar)
			mensaje = "Cuento eliminado"
			return redirect('config', permanent=False)
		else:
			rutaeliminar = colaborador.logo.path
			template = 'cuentos/eliminarcolaborador.html'
			book = {'colaborador':colaborador}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def colaboradorAgregar(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = ColaboradorForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
			else:
				error=True
		form = ColaboradorForm()
		return render(request, 'cuentos/agregarcolaborador.html', {'form':form})
	else:
		return redirect('listaCuentos', permanent=False)
