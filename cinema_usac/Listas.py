class Nodo:
    def __init__(self, pelicula, siguiente=None, anterior=None):
        self.pelicula = pelicula
        self.siguiente = siguiente
        self.anterior = anterior

class ListaDobleCircular:
    def __init__(self):
        self.primero = None

    def esta_vacia(self):
        return self.primero is None

    def agregar(self, pelicula):
        nuevo_nodo = Nodo(pelicula)

        if self.esta_vacia():
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
            self.primero = nuevo_nodo
        else:
            ultimo = self.primero.anterior
            nuevo_nodo.siguiente = self.primero
            nuevo_nodo.anterior = ultimo
            self.primero.anterior = nuevo_nodo
            ultimo.siguiente = nuevo_nodo

    def obtener_peliculas(self):
        peliculas = []
        if not self.esta_vacia():
            nodo_actual = self.primero
            while True:
                peliculas.append(nodo_actual.pelicula)
                nodo_actual = nodo_actual.siguiente
                if nodo_actual == self.primero:
                    break
        return peliculas
    