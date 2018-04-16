"""orotopia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
	path('', listaCuentos, name='listaCuentos'),
	path('<int:cuentoid>/ver/', verCuento, name='vercuento'),
	path('agregar/', agregarCuento, name='agregarcuento'),
	path('<int:cuentoid>/paginas/agregar/', agregarPagina, name='agregarpagina'),
	path('<int:cuentoid>/editar/titulo/', editarTituloCuento, name='editarTituloCuento'),
	path('<int:cuentoid>/editar/descripcion/', editarDescripcionCuento, name='editarDescripcionCuento'),
	path('<int:cuentoid>/editar/portada/', editarPortadaCuento, name='editarPortadaCuento'),
	path('<int:cuentoid>/eliminar/', eliminarCuento, name='eliminarCuento'),
	path('<int:cuentoid>/paginas/', listaPaginas, name='listaPaginas'),
	path('<int:cuentoid>/paginas/<int:paginaid>/editar/imagen/', editarImagenPagina, name='editarImagenPagina'),
	path('<int:cuentoid>/paginas/<int:paginaid>/editar/audio/', editarAudioPagina, name='editarAudioPagina'),
	path('<int:cuentoid>/paginas/<int:paginaid>/eliminar/', eliminarPagina, name='eliminarPagina'),
	path('<int:cuentoid>/paginas/erroreliminar/', errorEliminarPagina, name='errorEliminarPagina'),
	path('config/', config, name='config'),
	path('config/banner/', bannerConfig, name='bannerConfig'),
	path('config/trama/', tramaConfig, name='tramaConfig'),
	path('config/colaborador/<int:colaboradorid>/logo/', colaboradorLogo, name='colaboradorLogo'),
	path('config/colaborador/<int:colaboradorid>/linea1/', colaboradorLinea1, name='colaboradorLinea1'),
	path('config/colaborador/<int:colaboradorid>/linea2/', colaboradorLinea2, name='colaboradorLinea2'),
	path('config/colaborador/<int:colaboradorid>/eliminar/', colaboradorEliminar, name='colaboradorEliminar'),
	path('config/colaborador/agregar/', colaboradorAgregar, name='colaboradorAgregar'),
]