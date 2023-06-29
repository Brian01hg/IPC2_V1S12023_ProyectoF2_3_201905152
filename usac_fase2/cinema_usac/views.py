
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Sala, Tarjeta, Categoria, Pelicula
from .forms import PeliculaForm, SalaForm, TarjetaForm
import xml.etree.ElementTree as ET
import os


#----------Registro--------
class NodoUsuario:
    def __init__(self, usuario):
        self.usuario = usuario
        self.siguiente = None

class ListaEnlazadaUsuarios:
    def __init__(self):
        self.cabeza = None

    def agregar(self, usuario):
        nuevo_nodo = NodoUsuario(usuario)
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



def actualizar_archivo_xml(lista):
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



def registro_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        contraseña = request.POST['contraseña']
        telefono = request.POST['telefono']

        usuario = Usuario(nombre=nombre, apellido=apellido, correo=correo, contraseña=contraseña, telefono=telefono)
        usuario.save()

        lista = ListaEnlazadaUsuarios()
        lista.agregar(usuario)

        actualizar_archivo_xml(lista)

        return redirect('inicio')

    return render(request, 'registro.html')


def modificar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == 'POST':
        nombre_nuevo = request.POST['nombre_nuevo']
        usuario.nombre = nombre_nuevo
        usuario.save()

        lista = ListaEnlazadaUsuarios()
        lista.agregar(usuario)

        actualizar_archivo_xml(lista)

        return redirect('inicio')

    return render(request, 'modificar.html', {'usuario': usuario})


def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == 'POST':
        usuario.delete()

        lista = ListaEnlazadaUsuarios()
        lista.agregar(usuario)

        actualizar_archivo_xml(lista)

        return redirect('inicio')

    return render(request, 'eliminar.html', {'usuario': usuario})

def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def inicio(request):
    usuarios = Usuario.objects.all()
    return render(request, 'inicio.html', {'usuarios': usuarios})

#-------------inicio de secion----------

def inicio_sesion(request):
    print (request.session.get('correo'))
    if 'correo' in request.session: 
        
        return render(request, 'inicio_sesion.html')

    else:
        if request.method == 'POST':
            correo = request.POST['correo']
            password = request.POST['password']

            request.session['correo'] = correo
                
            return redirect('inicio')
        
        return render(request, 'inicio.html')
    

#---------------------peliculas-------------------
class NodoPelicula:
    def __init__(self, pelicula):
        self.pelicula = pelicula
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazadaCircular:
    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, pelicula):
        nuevo_nodo = NodoPelicula(pelicula)

        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
        else:
            ultimo_nodo = self.cabeza.anterior
            nuevo_nodo.siguiente = self.cabeza
            nuevo_nodo.anterior = ultimo_nodo
            self.cabeza.anterior = nuevo_nodo
            ultimo_nodo.siguiente = nuevo_nodo

    def buscar_nodo(self, nombre):
        if self.esta_vacia():
            return None

        actual = self.cabeza
        while True:
            if actual.pelicula.nombre == nombre:
                return actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return None

    def eliminar(self, nodo):
        if self.esta_vacia():
            return

        if self.cabeza == nodo:
            if self.cabeza.siguiente == self.cabeza:
                self.cabeza = None
            else:
                ultimo_nodo = self.cabeza.anterior
                siguiente_nodo = self.cabeza.siguiente
                siguiente_nodo.anterior = ultimo_nodo
                ultimo_nodo.siguiente = siguiente_nodo
                self.cabeza = siguiente_nodo
        else:
            nodo.anterior.siguiente = nodo.siguiente
            nodo.siguiente.anterior = nodo.anterior

        nodo.siguiente = None
        nodo.anterior = None

# Crear instancia de la lista doblemente enlazada circular
lista_peliculas = ListaDoblementeEnlazadaCircular()

def generar_xml_peliculas():
    root = ET.Element('Peliculas')

    if lista_peliculas.cabeza:
        actual = lista_peliculas.cabeza
        while True:
            pelicula = actual.pelicula
            pelicula_xml = ET.SubElement(root, 'Pelicula')
            ET.SubElement(pelicula_xml, 'Titulo').text = pelicula.titulo
            ET.SubElement(pelicula_xml, 'Descripcion').text = pelicula.descripcion
            ET.SubElement(pelicula_xml, 'Anio').text = str(pelicula.anio)
            ET.SubElement(pelicula_xml, 'Categoria').text = pelicula.categoria.nombre

            actual = actual.siguiente
            if actual == lista_peliculas.cabeza:
                break

    xml_tree = ET.ElementTree(root)
    xml_tree.write('peliculas.xml')

# Vista para agregar una película
def crear_pelicula(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        anio = int(request.POST['anio'])
        categoria_id = int(request.POST['categoria'])

        # Obtener la categoría correspondiente
        categoria = get_object_or_404(Categoria, pk=categoria_id)

        # Crear la instancia de Pelicula y guardarla en la base de datos
        pelicula = Pelicula(titulo=titulo, descripcion=descripcion, anio=anio, categoria=categoria)
        pelicula.save()

        # Agregar la película a la lista doblemente enlazada circular
        lista_peliculas.agregar(pelicula)

        # Generar el archivo XML de películas
        generar_xml_peliculas()

        return redirect('lista_peliculas')

    categorias = Categoria.objects.all()
    return render(request, 'crear_pelicula.html', {'categorias': categorias})

# Vista para modificar una película
def modificar_pelicula(request, id):
    pelicula = get_object_or_404(Pelicula, pk=id)

    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo_nuevo = request.POST['titulo']
        descripcion_nueva = request.POST['descripcion']
        anio_nuevo = int(request.POST['anio'])
        categoria_id = int(request.POST['categoria'])

        # Obtener la categoría correspondiente
        categoria = get_object_or_404(Categoria, pk=categoria_id)

        # Modificar los datos de la película
        pelicula.titulo = titulo_nuevo
        pelicula.descripcion = descripcion_nueva
        pelicula.anio = anio_nuevo
        pelicula.categoria = categoria
        pelicula.save()

        # Generar el archivo XML de películas
        generar_xml_peliculas()

        return redirect('lista_peliculas')

    categorias = Categoria.objects.all()
    return render(request, 'modificar_pelicula.html', {'pelicula': pelicula, 'categorias': categorias})

# Vista para eliminar una película
def eliminar_pelicula(request, id):
    pelicula = get_object_or_404(Pelicula, pk=id)

    if request.method == 'POST':
        # Eliminar la película de la base de datos
        pelicula.delete()

        # Eliminar la película de la lista doblemente enlazada circular
        nodo_pelicula = lista_peliculas.buscar_nodo(pelicula)
        if nodo_pelicula:
            lista_peliculas.eliminar(nodo_pelicula)

        # Generar el archivo XML de películas
        generar_xml_peliculas()

        return redirect('lista_peliculas')

    return render(request, 'eliminar_pelicula.html', {'pelicula': pelicula})

# Vista para listar todas las películas
def lista_peliculas(request):
    peliculas = []
    if lista_peliculas.cabeza:
        actual = lista_peliculas.cabeza
        while True:
            peliculas.append(actual.pelicula)
            actual = actual.siguiente
            if actual == lista_peliculas.cabeza:
                break

    return render(request, 'lista_peliculas.html', {'peliculas': peliculas})



def agregar_pelicula(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = PeliculaForm()
    return render(request, 'agregar_pelicula.html', {'form': form})

#----------Salas-----------------------

class NodoSalas:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazadaSalas:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def insertar_al_final(self, dato):
        nuevo_nodo = NodoSalas(dato)
        if not self.primero:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.ultimo
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo

    def obtener_salas(self):
        salas = []
        nodo_actual = self.primero
        while nodo_actual:
            salas.append(nodo_actual.dato)
            nodo_actual = nodo_actual.siguiente
        return salas
    
    def obtener_tarjetas(self):
        tarjetas = []
        nodo_actual = self.primero
        while nodo_actual:
            tarjetas.append(nodo_actual.dato)
            nodo_actual = nodo_actual.siguiente
        return tarjetas
    
def gestionar_salas(request):
    # Crear y gestionar la lista doblemente enlazada
    lista_salas = ListaDoblementeEnlazadaSalas()
    lista_salas.insertar_al_final(Sala(numero='#USACIPC2_202212333_1', asientos=100))
    lista_salas.insertar_al_final(Sala(numero='#USACIPC2_202212333_2', asientos=80))
    lista_salas.insertar_al_final(Sala(numero='#USACIPC2_202212333_3', asientos=120))

    # Obtener las salas de la lista
    salas = lista_salas.obtener_salas()

    # Generar el archivo XML de ejemplo
    root = ET.Element('cines')
    cine_element = ET.SubElement(root, 'cine')
    nombre_element = ET.SubElement(cine_element, 'nombre')
    nombre_element.text = 'Cine ABC'

    salas_element = ET.SubElement(cine_element, 'salas')
    for sala in salas:
        sala_element = ET.SubElement(salas_element, 'sala')
        numero_element = ET.SubElement(sala_element, 'numero')
        numero_element.text = sala.numero
        asientos_element = ET.SubElement(sala_element, 'asientos')
        asientos_element.text = str(sala.asientos)

    tree = ET.ElementTree(root)
    xml_path = 'salas.xml'
    tree.write(xml_path)

    # Renderizar la plantilla HTML
    context = {
        'salas': salas,
        'xml_path': xml_path,
    }
    return render(request, 'salas.html', context)

def modificar_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)

    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = SalaForm(instance=sala)

    return render(request, 'modificar_sala.html', {'form': form})

def agregar_sala(request, cine_id):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            sala = form.save(commit=False)
            sala.cine_id = cine_id
            sala.save()
            return redirect('inicio')
    else:
        form = SalaForm()

    return render(request, 'agregar_sala.html', {'form': form})

def eliminar_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)

    if request.method == 'POST':
        sala.delete()
        return redirect('inicio')

    return render(request, 'eliminar_sala.html', {'sala': sala})

#------------tarjetas--------------------

def gestionar_tarjetas(request):
    # Crear y gestionar la lista doblemente enlazada
    lista_tarjetas = ListaDoblementeEnlazadaSalas()
    lista_tarjetas.insertar_al_final(Tarjeta(tipo='Débito', numero='123456789', titular='John Doe', fecha_expiracion='01/25'))
    lista_tarjetas.insertar_al_final(Tarjeta(tipo='Crédito', numero='987654321', titular='Jane Smith', fecha_expiracion='03/27'))
    lista_tarjetas.insertar_al_final(Tarjeta(tipo='Débito', numero='567891234', titular='Alice Johnson', fecha_expiracion='12/24'))

    # Obtener las tarjetas de la lista
    tarjetas = lista_tarjetas.obtener_tarjetas()

    # Renderizar la plantilla HTML
    context = {
        'tarjetas': tarjetas,
    }
    return render(request, 'tarjetas.html', context)

def eliminar_tarjeta(request, tarjeta_id):
    tarjeta = get_object_or_404(Tarjeta, id=tarjeta_id)

    if request.method == 'POST':
        tarjeta.delete()
        return redirect('tarjetas')

    return render(request, 'eliminar_tarjeta.html', {'tarjeta': tarjeta})

def modificar_tarjeta(request, tarjeta_id):
    tarjeta = get_object_or_404(Tarjeta, id=tarjeta_id)

    if request.method == 'POST':
        form = TarjetaForm(request.POST, instance=tarjeta)
        if form.is_valid():
            form.save()
            return redirect('tarjetas')
    else:
        form = TarjetaForm(instance=tarjeta)

    return render(request, 'modificar_tarjeta.html', {'form': form})

def agregar_tarjeta(request):
    if request.method == 'POST':
        form = TarjetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tarjetas')
    else:
        form = TarjetaForm()

    return render(request, 'agregar_tarjeta.html', {'form': form})

#--------------------Boletos-----------------
