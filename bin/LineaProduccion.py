class LineaProduccion():

    def __init__(self, numero, cantidadComponentes, tiempoEnsamblaje):
        self.numero = int(numero)
        self.cantidadComponentes = int(cantidadComponentes)
        self.tiempoEnsamblaje = int(tiempoEnsamblaje)

    def getNumero(self):
        return self.numero

    def getCantidadComponentes(self):
        return self.cantidadComponentes

    def getTiempoEnsamblaje(self):
        return self.tiempoEnsamblaje