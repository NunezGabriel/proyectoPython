class Nodo:
    def __init__(self, vehiculo):
        self.vehiculo = vehiculo
        self.ant = None
        self.sig = None

class ListaDoble:
    def __init__(self):
        self.inicio = None
        self.fin = None

    def insertar(self, vehiculo):
        nuevo = Nodo(vehiculo)
        if self.inicio is None:
            self.inicio = self.fin = nuevo
        else:
            self.fin.sig = nuevo
            nuevo.ant = self.fin
            self.fin = nuevo

    def eliminar(self, placa):
        actual = self.inicio
        while actual:
            if actual.vehiculo.placa == placa:
                if actual.ant:
                    actual.ant.sig = actual.sig
                else:
                    self.inicio = actual.sig
                if actual.sig:
                    actual.sig.ant = actual.ant
                else:
                    self.fin = actual.ant
                return actual.vehiculo
            actual = actual.sig
        return None

    def listar(self):
        actual = self.inicio
        vehiculos = []
        while actual:
            vehiculos.append(actual.vehiculo)
            actual = actual.sig
        return vehiculos
