class Vehiculo:
    def __init__(self, placa, marca, color, conductor):
        self.placa = placa
        self.marca = marca
        self.color = color
        self.conductor = conductor
        self.hora_entrada = None
        self.hora_salida = None
        self.tipo_vehiculo = "Genérico"

class Auto(Vehiculo):
    def __init__(self, placa, marca, color, conductor):
        super().__init__(placa, marca, color, conductor)
        self.tipo_vehiculo = "Auto"

class Moto(Vehiculo):
    def __init__(self, placa, marca, color, conductor, cilindrada):
        super().__init__(placa, marca, color, conductor)
        self.cilindrada = cilindrada
        self.tipo_vehiculo = "Moto"

class Bicicleta(Vehiculo):
    def __init__(self, marca, color, conductor, modelo):
        super().__init__("BIC-" + conductor.dni[-4:], marca, color, conductor)
        self.modelo = modelo
        self.tipo_vehiculo = "Bicicleta"