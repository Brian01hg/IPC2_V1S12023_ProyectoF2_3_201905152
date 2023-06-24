from django.db import models

# Create your models here.
class Carrusel(models.Model):
    imagen = models.ImageField(upload_to='pics/%y/%m/%d')
    titulo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.titulo


class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='peliculas/')

    def __str__(self):
        return self.titulo

class Usuario(models.Model):
    
    nombre = models.TextField(max_length=100)
    apellido = models.TextField(max_length=100)
    correo = models.TextField(max_length=100)
    contraseña = models.TextField(max_length=100)
    telefono = models.TextField(max_length=100)

class Imagen(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo