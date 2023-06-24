from django.shortcuts import render, redirect
from .models import Usuario, Pelicula
from .Listas import ListaDobleCircular
import xml.etree.ElementTree as ET

#--------Peliculas---------------

def carrusel(request):
    peliculas = Pelicula.objects.all()
    carrusel_peliculas = ListaDobleCircular()

    for pelicula in peliculas:
        carrusel_peliculas.agregar(pelicula)

    context = {
        'peliculas': carrusel_peliculas.obtener_peliculas()
    }

    return render(request, 'carrusel.html', context)


#----------Registro--------
class Nodo:
    def __init__(self, usuario):
        self.usuario = usuario
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, usuario):
        nuevo_nodo = Nodo(usuario)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def buscar_nodo(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.usuario.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None

    def eliminar(self, nodo):
        if self.cabeza == nodo:
            self.cabeza = self.cabeza.siguiente
        else:
            actual = self.cabeza
            while actual.siguiente != nodo:
                actual = actual.siguiente
            actual.siguiente = nodo.siguiente

# Create your views here.
def registro_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        contraseña = request.POST['contraseña']
        telefono = request.POST['telefono']
        # Crea una instancia del modelo Usuario y guarda los datos
        usuario = Usuario(nombre=nombre, apellido=apellido, correo=correo, contraseña=contraseña, telefono=telefono)
        usuario.save()
        
 
        lista = ListaEnlazada()
        lista.agregar(usuario)

        # Genera el archivo XML a partir de la lista enlazada
        root = ET.Element('Usuarios')
        actual = lista.cabeza
        while actual is not None:
            usuario_xml = ET.SubElement(root, 'Usuario')
            ET.SubElement(usuario_xml, 'Nombre').text = actual.usuario.nombre
            ET.SubElement(usuario_xml, 'Apellido').text = actual.usuario.apellido
            ET.SubElement(usuario_xml, 'Correo').text = actual.usuario.correo
            ET.SubElement(usuario_xml, 'Contraseña').text = actual.usuario.contraseña
            ET.SubElement(usuario_xml, 'Telefono').text = actual.usuario.telefono
            actual = actual.siguiente

        xml_tree = ET.ElementTree(root)
        xml_tree.write('usuarios.xml')

        return redirect('inicio')

    return render(request, 'registro.html')


def inicio(request):
    usuarios = Usuario.objects.all()
    return render(request, 'inicio.html', {'usuarios': usuarios})

def modificar_usuario(request, id):
    usuario = Usuario.objects.get(pk=id)

    if request.method == 'POST':
        nombre_nuevo = request.POST['nombre_nuevo']
        usuario.nombre = nombre_nuevo
        usuario.save()

        # Actualizar el archivo XML si es necesario

        return redirect('inicio')

    return render(request, 'modificar.html', {'usuario': usuario})

def eliminar_usuario(request, id):
    usuario = Usuario.objects.get(pk=id)

    if request.method == 'POST':
        usuario.delete()

        # Actualizar el archivo XML si es necesario

        return redirect('inicio')

    return render(request, 'eliminar.html', {'usuario': usuario})

