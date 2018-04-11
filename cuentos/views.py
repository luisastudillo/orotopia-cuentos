from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import redirect

# Create your views here.

def redirectListaCuentos(request):
	return redirect('listaCuentos', permanent=False)

def listaCuentos(request):
	listacuentos = Cuento.objects.all()
	listacolabs = Colaborador.objects.all()
	config = Config.objects.get(id=1)
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

def editarCuento(request, cuentoid):
	if request.user.is_staff:
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			form=CuentoForm(request.POST,instance=cuento)
			if form.is_valid():
				form.save()
				mensaje = "Cambios guardados"
				return redirect('listaCuentos', permanent=False)
		else:
			form=CuentoForm(instance=cuento)
			template = 'cuentos/editarCuento.html'
			book = {'form':form}
			return render(request, template, book)
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
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			form=PortadaCuentoForm(request.POST,instance=cuento)
			if form.is_valid():
				form.save()
				mensaje = "Cambios guardados"
				return redirect('listaPaginas', cuentoid)
		else:
			form=PortadaCuentoForm(instance=cuento)
			titulo=cuento.titulo
			template = 'cuentos/editarportadacuento.html'
			book = {'form':form, 'titulo':titulo, 'cuento':cuento}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def editarPagina(request, cuentoid, paginaid):
	if request.user.is_staff:
		pagina = Pagina.objects.get(id=paginaid)
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			form=PaginaForm(request.POST, request.FILES, instance=pagina)
			if form.is_valid():
				print("Bien bien")
				form.save()
				mensaje = "Cambios guardados"
				return redirect('listaPaginas', cuentoid)
			else:
				print("mal mal")
		else:
			form=PaginaForm(instance=pagina)
			template = 'cuentos/editarPagina.html'
			book = {'form':form, 'cuento':cuento, 'pagina':pagina}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def editarImagenPagina(request, cuentoid, paginaid):
	if request.user.is_staff:
		pagina = Pagina.objects.get(id=paginaid)
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			form=ImagenPaginaForm(request.POST, request.FILES, instance=pagina)
			if form.is_valid():
				form.save()
				pagina.dividir()
				pagina.save()
				mensaje = "Cambios guardados"
				return redirect('listaPaginas', cuentoid)
			else:
				print("mal mal")
		else:
			form=ImagenPaginaForm(instance=pagina)
			template = 'cuentos/cambiarimagenpagina.html'
			book = {'form':form, 'cuento':cuento, 'pagina':pagina}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def editarAudioPagina(request, cuentoid, paginaid):
	if request.user.is_staff:
		pagina = Pagina.objects.get(id=paginaid)
		cuento = Cuento.objects.get(id=cuentoid)
		if request.POST:
			form=ImagenPaginaForm(request.POST, request.FILES, instance=pagina)
			if form.is_valid():
				form.save()
				mensaje = "Cambios guardados"
				return redirect('listaPaginas', cuentoid)
			else:
				print("mal mal")
		else:
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
			cuento.delete()
			mensaje = "Cuento eliminado"
			return redirect('listaCuentos', permanent=False)
		else:
			template = 'cuentos/eliminarCuento.html'
			book = {'cuento':cuento}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def eliminarPagina(request, cuentoid, paginaid):
	if request.user.is_staff:
		cuento = Cuento.objects.get(id=cuentoid)
		pagina = Pagina.objects.get(id=paginaid)
		if request.POST:
			pagina.delete()
			return redirect('listaPaginas', cuentoid,  permanent=False)
		else:
			template = 'cuentos/eliminarpagina.html'
			book = {'cuento':cuento, 'pagina':pagina}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def listaPaginas(request, cuentoid):
	lista = Pagina.objects.filter(cuento=cuentoid)
	cuento = Cuento.objects.get(id=cuentoid)
	return render(request, 'cuentos/listapaginas.html', {'lista': lista, 'cuento':cuento})

def config(request):
	lista = Colaborador.objects.all()
	config = Config.objects.get(id=1)
	return render(request, 'cuentos/config.html', {'lista': lista, 'config':config})

def bannerConfig(request):
	if request.user.is_staff:
		config = Config.objects.get(id=1)
		if request.POST:
			form=BannerConfigForm(request.POST, request.FILES, instance=config)
			if form.is_valid():
				form.save()
				config.save()
				mensaje = "Cambios guardados"
				return redirect('config')
			else:
				print("mal mal")
		else:
			form=BannerConfigForm(instance=config)
			template = 'cuentos/bannerconfig.html'
			book = {'form':form, 'config':config}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def tramaConfig(request):
	if request.user.is_staff:
		config = Config.objects.get(id=1)
		if request.POST:
			form=TramaConfigForm(request.POST, request.FILES, instance=config)
			if form.is_valid():
				form.save()
				config.save()
				mensaje = "Cambios guardados"
				return redirect('config')
			else:
				print("mal mal")
		else:
			form=TramaConfigForm(instance=config)
			template = 'cuentos/tramaconfig.html'
			book = {'form':form, 'config':config}
			return render(request, template, book)
	else:
		return redirect('listaCuentos', permanent=False)

def colaboradorLogo(request, colaboradorid):
	if request.user.is_staff:
		colaborador = Colaborador.objects.get(id=colaboradorid)
		if request.POST:
			form=LogoColaboradorForm(request.POST, request.FILES, instance=colaborador)
			if form.is_valid():
				form.save()
				colaborador.save()
				mensaje = "Cambios guardados"
				return redirect('config')
			else:
				print("mal mal")
		else:
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
				colaborador.save()
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
				colaborador.save()
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
		colaborador = Colaborador.objects.get(id=colaboradorid)
		if request.POST:
			colaborador.delete()
			mensaje = "Cuento eliminado"
			return redirect('config', permanent=False)
		else:
			template = 'cuentos/eliminarColaborador.html'
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
