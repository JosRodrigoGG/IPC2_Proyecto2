from bin.Lista import Lista


class Producto:

    def __init__(self, nombre):
        self.nombre = str(nombre)
        self.elaboracion = Lista()

    def getNombre(self):
        return self.nombre

    def getLista(self):
        return self.elaboracion
    
    def agregarElaboracion(self, dato):
        self.elaboracion.agregar(str(dato))