import tkinter as tk
from tkinter import messagebox
from vehiculo import Vehiculo
from conductor import Conductor
from parking import Parking

parking = Parking(10)  # capacidad inicial

def actualizar_lista():
    lista_vehiculos.delete(0, tk.END)  # Limpiamos la lista
    for v in parking.obtener_vehiculos():
        texto = f"{v.placa} - {v.marca} - {v.conductor.nombre}"
        lista_vehiculos.insert(tk.END, texto)

def registrar_entrada():
    nombre = entry_nombre.get()
    dni = entry_dni.get()
    tipo = tipo_var.get()
    placa = entry_placa.get()
    marca = entry_marca.get()
    color = entry_color.get()

    conductor = Conductor(nombre, dni, tipo)
    vehiculo = Vehiculo(placa, marca, color, conductor)
    if parking.registrar_ingreso(vehiculo):
        messagebox.showinfo("Éxito", "Vehículo ingresado correctamente")
        actualizar_lista()
    else:
        messagebox.showerror("Error", "Parking lleno")

def registrar_salida():
    placa = entry_placa.get()
    vehiculo = parking.registrar_salida(placa)
    if vehiculo:
        pago = parking.calcular_pago(vehiculo)
        messagebox.showinfo("Salida", f"Pago total: S/ {pago}")
        actualizar_lista()
    else:
        messagebox.showerror("Error", "Vehículo no encontrado")

ventana = tk.Tk()
ventana.title("Gestión de Parking Tecsup")
ventana.geometry("400x600")
ventana.configure(bg="#0f4c81")

tk.Label(ventana, text="Nombre:", bg="#0f4c81", fg="white").pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()

tk.Label(ventana, text="DNI:", bg="#0f4c81", fg="white").pack()
entry_dni = tk.Entry(ventana)
entry_dni.pack()

tk.Label(ventana, text="Tipo:", bg="#0f4c81", fg="white").pack()
tipo_var = tk.StringVar(value="estudiante")
tk.Radiobutton(ventana, text="Estudiante", variable=tipo_var, value="estudiante").pack()
tk.Radiobutton(ventana, text="Profesor", variable=tipo_var, value="profesor").pack()

tk.Label(ventana, text="Placa:", bg="#0f4c81", fg="white").pack()
entry_placa = tk.Entry(ventana)
entry_placa.pack()

tk.Label(ventana, text="Marca:", bg="#0f4c81", fg="white").pack()
entry_marca = tk.Entry(ventana)
entry_marca.pack()

tk.Label(ventana, text="Color:", bg="#0f4c81", fg="white").pack()
entry_color = tk.Entry(ventana)
entry_color.pack()

tk.Button(ventana, text="Registrar Entrada", command=registrar_entrada).pack(pady=10)
tk.Button(ventana, text="Registrar Salida", command=registrar_salida).pack(pady=10)

# Lista de vehículos en el parking
tk.Label(ventana, text="Vehículos en el Parking:", bg="#0f4c81", fg="white").pack(pady=(20,5))
lista_vehiculos = tk.Listbox(ventana, width=50)
lista_vehiculos.pack(pady=5)

ventana.mainloop()
