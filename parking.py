import time
from listas import ListaDoble

class Parking:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.ocupados = 0
        self.vehiculos = ListaDoble()

    def hay_espacio(self):
        return self.ocupados < self.capacidad

    def registrar_ingreso(self, vehiculo):
        if self.hay_espacio():
            vehiculo.hora_entrada = time.time()
            self.vehiculos.insertar(vehiculo)
            self.ocupados += 1
            return True
        return False

    def registrar_salida(self, placa):
        vehiculo = self.vehiculos.eliminar(placa)
        if vehiculo:
            vehiculo.hora_salida = time.time()
            self.ocupados -= 1
            return vehiculo
        return None

    def calcular_pago(self, vehiculo):
        if vehiculo.conductor.tipo == "profesor":
            return 0
        tiempo = (vehiculo.hora_salida - vehiculo.hora_entrada) / 60  # minutos
        return round(tiempo * 0.5, 2)  # 0.5 soles por minuto 

    def obtener_vehiculos(self):
        return self.vehiculos.listar()
