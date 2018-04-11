from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Cuento)
admin.site.register(Pagina)

