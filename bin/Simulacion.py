from bin.Lista import Lista

class Simulacion:

    def __init__(self, nombre):
        self.nombre = nombre
        self.listaProductos = Lista()

    def getNombre(self):
        return self.nombre

    def getListaProductos(self):
        return self.listaProductos

    def agregarProductos(self, dato):
        self.listaProductos.agregar(dato)