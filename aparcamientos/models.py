from django.db import models
from django.contrib import admin


# Create your models here.
class Aparcamiento(models.Model):
    identificador = models.CharField(max_length = 10, blank=True)
    nombre = models.CharField(max_length=200,  blank = True)
    descripcion = models.TextField(blank = True)
    access = models.BooleanField(default=False)
    url = models.CharField(max_length=200, blank = True)
    calle = models.CharField(max_length=100, blank=True)
    numero_via = models.CharField(max_length=100, blank=True)
    localidad = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=30, blank = True)
    codigo_postal = models.CharField(max_length = 10,  blank = True)
    barrio = models.CharField(max_length=200, blank = True)
    distrito = models.CharField(max_length=200, blank = True)
    latitud = models.CharField(max_length=200, blank = True)
    longitud = models.CharField(max_length=200, blank = True)
    tlf = models.CharField(max_length=200, blank = True)
    mail = models.CharField(max_length = 200, blank = True)
