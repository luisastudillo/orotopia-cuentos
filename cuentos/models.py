from django.db import models
# Import Pillow:
from PIL import Image

class Cuento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    n_paginas = models.IntegerField(default=0)
    portada = models.ImageField(upload_to='imagenes/')
    def __unicode__(self):
    	return self.titulo

class Pagina(models.Model):
    cuento = models.ForeignKey(Cuento, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/')
    imagen1 = models.ImageField(upload_to='imagenes/', blank=True)
    imagen2 = models.ImageField(upload_to='imagenes/', blank=True)
    audio = models.FileField(upload_to='audios/')
    numero = models.IntegerField(default=0, blank=True)
    def __unicode__(self):
    	return self.cuento
    def numerar(self):
    	cuento = Cuento.objects.get(id=self.cuento.id)
    	pagina = cuento.n_paginas
    	pagina=pagina+1
    	self.numero = pagina
    	cuento.n_paginas = pagina
    	cuento.save()
    def dividir(self):
        imagen = self.imagen
        img = Image.open(imagen)
        width = img.size[0]
        height = img.size[1]
        path= imagen.path
        ext = path[-4:]
        path1 = path[:-4] + "1" + ext
        path2 = path[:-4] + "2" + ext
        print("url: " + path)
        print("path1: " + path1)
        print("path2: " + path2)
        img1 = img.crop((0, 0, width, height/2))
        img1.save(path1)
        img2 = img.crop((0, height/2, width, height))
        img2.save(path2)
        self.imagen1=path1
        self.imagen2=path2
