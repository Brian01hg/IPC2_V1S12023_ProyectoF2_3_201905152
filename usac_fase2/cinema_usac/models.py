from django.db import models

# Create your models here.

class Pelicula(models.Model):
    titulo = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    anio = models.IntegerField()
    fecha = models.DateField()
    hora = models.TimeField()
    imagen = models.URLField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.titulo


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    peliculas = models.ManyToManyField(Pelicula)

    def __str__(self):
        return self.nombre
    
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
    
class Sala(models.Model):
    numero = models.CharField(max_length=50)
    asientos = models.IntegerField()

    def __str__(self):
        return self.numero
    
class Cine(models.Model):
    nombre = models.CharField(max_length=50)
    salas = models.ManyToManyField(Sala)

    def __str__(self):
        return self.nombre
    
class Tarjeta(models.Model):
    TIPO_CHOICES = [
        ('Debito', 'Débito'),
        ('Credito', 'Crédito'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    numero = models.CharField(max_length=16)
    titular = models.CharField(max_length=100)
    fecha_expiracion = models.CharField(max_length=7)

    def __str__(self):
        return self.numero
    

    