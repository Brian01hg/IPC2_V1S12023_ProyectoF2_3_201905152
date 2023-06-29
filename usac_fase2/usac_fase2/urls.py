"""
URL configuration for usac_fase2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from cinema_usac.views import registro_usuario, modificar_usuario, inicio, eliminar_usuario, inicio_sesion
from cinema_usac.views import agregar_pelicula, gestionar_salas, modificar_sala, agregar_sala, eliminar_sala, gestionar_tarjetas, modificar_tarjeta, eliminar_tarjeta, agregar_tarjeta
from cinema_usac.views import lista_usuarios, lista_peliculas, crear_pelicula, modificar_pelicula, eliminar_pelicula, agregar_sala

urlpatterns = [

    path('admin/', admin.site.urls),
    path('inicio/', inicio, name='inicio'),
    path('registro/', registro_usuario, name='registro'),
    path('iniciode/', inicio_sesion, name='iniciode'),
    path('modificar/<int:id>/', modificar_usuario, name='modificar'),
    path('eliminar/<int:id>/', eliminar_usuario, name='eliminar'),
    path('agregar_pelicula/', agregar_pelicula, name='agregar_pelicula'),
    path('gestionar-salas/', gestionar_salas, name='gestionar_salas'),
    path('sala/modificar/<int:sala_id>/', modificar_sala, name='modificar_sala'),
    path('sala/agregar/<int:cine_id>/', agregar_sala, name='agregar_sala'),
    path('sala/eliminar/<int:sala_id>/', eliminar_sala, name='eliminar_sala'),
    path('tarjetas/', gestionar_tarjetas, name='tarjetas'),
    path('tarjetas/eliminar/<int:tarjeta_id>/', eliminar_tarjeta, name='eliminar_tarjeta'),
    path('tarjetas/modificar/<int:tarjeta_id>/', modificar_tarjeta, name='modificar_tarjeta'),
    path('tarjetas/agregar/', agregar_tarjeta, name='agregar_tarjeta'),
    path('lista_usuarios/', lista_usuarios, name='lista_usuarios'),
    path('base/', lista_peliculas, name='lista_peliculas'),
    path('agregar/', crear_pelicula, name='agregar_pelicula'),
    path('modificar/<int:id>/', modificar_pelicula, name='modificar_pelicula'),
    path('eliminar/<int:id>/', eliminar_pelicula, name='eliminar_pelicula'),
    path('cine/<int:cine_id>/agregar_sala/', agregar_sala, name='agregar_sala'),


    
]