from bin.Lista import Lista

class Maquina():

    def __init__(self, cantidadLineas):
        self.cantidadLineasProduccion = int(cantidadLineas)
        self.lineasProduccion = Lista()
        self.productos = Lista()

    def getCantidadLineasProduccion(self):
        return self.cantidadLineasProduccion

    def getLineasProduccion(self):
        return self.lineasProduccion

    def getProductos(self):
        return self.productos

    def agregarLineasProduccion(self,dato):
        self.lineasProduccion.agregar(dato)

    def agregarProducto(self, dato):
        self.productos.agregar(dato)