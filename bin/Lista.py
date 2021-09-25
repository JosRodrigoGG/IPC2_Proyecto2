from bin.Nodo import Nodo

class Lista:

    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.cantidad = 0

    def vacia(self):
        return self.primero is None

    def getCantidad(self):
        return self.cantidad

    def getPrimero(self):
        return self.primero

    def agregar(self, dato):
        if self.vacia():
            self.primero = self.ultimo = Nodo(dato)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = Nodo(dato)
            self.ultimo.anterior = aux
        self._unirNodos()
        self.cantidad += 1

    def _unirNodos(self):
        self.primero.anterior = self.ultimo
        self.ultimo.siguiente = self.primero