import time
from listas import ListaDoble

class Parking:
    def __init__(self, capacidad_autos, capacidad_motos, capacidad_bicis):
        self.capacidad_autos = capacidad_autos
        self.capacidad_motos = capacidad_motos
        self.capacidad_bicis = capacidad_bicis
        self.ocupados_autos = 0
        self.ocupados_motos = 0
        self.ocupados_bicis = 0
        self.vehiculos = ListaDoble()

    def hay_espacio(self, tipo_vehiculo):
        if tipo_vehiculo == "Auto":
            return self.ocupados_autos < self.capacidad_autos
        elif tipo_vehiculo == "Moto":
            return self.ocupados_motos < self.capacidad_motos
        elif tipo_vehiculo == "Bicicleta":
            return self.ocupados_bicis < self.capacidad_bicis
        return False

    def registrar_ingreso(self, vehiculo):
        if self.hay_espacio(vehiculo.tipo_vehiculo):
            vehiculo.hora_entrada = time.time()
            self.vehiculos.insertar(vehiculo)
            
            if vehiculo.tipo_vehiculo == "Auto":
                self.ocupados_autos += 1
            elif vehiculo.tipo_vehiculo == "Moto":
                self.ocupados_motos += 1
            elif vehiculo.tipo_vehiculo == "Bicicleta":
                self.ocupados_bicis += 1
                
            return True
        return False

    def registrar_salida(self, placa):
        vehiculo = self.vehiculos.eliminar(placa)
        if vehiculo:
            vehiculo.hora_salida = time.time()
            
            if vehiculo.tipo_vehiculo == "Auto":
                self.ocupados_autos -= 1
            elif vehiculo.tipo_vehiculo == "Moto":
                self.ocupados_motos -= 1
            elif vehiculo.tipo_vehiculo == "Bicicleta":
                self.ocupados_bicis -= 1
                
            return vehiculo
        return None

    def calcular_pago(self, vehiculo):
        if vehiculo.conductor.tipo == "profesor":
            return 0
            
        tiempo = (vehiculo.hora_salida - vehiculo.hora_entrada) / 60  # minutos
        
        # Tarifas diferenciadas
        if vehiculo.tipo_vehiculo == "Auto":
            return round(tiempo * 0.5, 2)  # 0.5 soles por minuto
        elif vehiculo.tipo_vehiculo == "Moto":
            return round(tiempo * 0.3, 2)  # 0.3 soles por minuto
        elif vehiculo.tipo_vehiculo == "Bicicleta":
            return round(tiempo * 0.1, 2)  # 0.1 soles por minuto

    def obtener_vehiculos(self):
        return self.vehiculos.listar()
    
    def obtener_estado(self):
        return {
            "autos": f"{self.ocupados_autos}/{self.capacidad_autos}",
            "motos": f"{self.ocupados_motos}/{self.capacidad_motos}",
            "bicicletas": f"{self.ocupados_bicis}/{self.capacidad_bicis}"
        }