import tkinter as tk
from tkinter import messagebox
from vehiculo import Vehiculo
from conductor import Conductor
from parking import Parking

parking = Parking(10)  # capacidad del parking

def lanzar_app():
    ventana = tk.Tk()  # <-- ESTO FALTABA (creamos la ventana principal)

    def mostrar_menu():
        limpiar_ventana()
        tk.Label(ventana, text="Tecsup Parking", font=("Helvetica", 18, "bold"), bg="#0f4c81", fg="white").pack(pady=30)

        tk.Button(ventana, text="Registrar Entrada", command=mostrar_entrada, width=20, height=2, bg="white").pack(pady=10)
        tk.Button(ventana, text="Registrar Salida", command=mostrar_salida, width=20, height=2, bg="white").pack(pady=10)
    def mostrar_entrada():
        limpiar_ventana()

        tk.Label(ventana, text="Registro de Entrada", font=("Helvetica", 14, "bold"), bg="#0f4c81", fg="white").pack(pady=10)

        # Formulario
        for text in ["Nombre:", "DNI:", "Placa:", "Marca:", "Color:"]:
            tk.Label(ventana, text=text, bg="#0f4c81", fg="white").pack()
        
        nombre = tk.Entry(ventana); nombre.pack()
        dni = tk.Entry(ventana); dni.pack()

        tk.Label(ventana, text="Tipo:", bg="#0f4c81", fg="white").pack()
        tipo_var = tk.StringVar(value="estudiante")
        tk.Radiobutton(ventana, text="Estudiante", variable=tipo_var, value="estudiante").pack()
        tk.Radiobutton(ventana, text="Profesor", variable=tipo_var, value="profesor").pack()

        placa = tk.Entry(ventana); placa.pack()
        marca = tk.Entry(ventana); marca.pack()
        color = tk.Entry(ventana); color.pack()

        def registrar():
            conductor = Conductor(nombre.get(), dni.get(), tipo_var.get())
            vehiculo = Vehiculo(placa.get(), marca.get(), color.get(), conductor)
            if parking.registrar_ingreso(vehiculo):
                messagebox.showinfo("Éxito", "Vehículo ingresado")
                actualizar_lista(lista)
                actualizar_estado()
            else:
                messagebox.showerror("Error", "Parking lleno")

        tk.Button(ventana, text="Registrar", command=registrar, bg="white").pack(pady=10)
        tk.Button(ventana, text="Volver al menú", command=mostrar_menu, bg="white").pack(pady=5)

        # Lista de vehículos
        tk.Label(ventana, text="Vehículos en Parking:", bg="#0f4c81", fg="white").pack(pady=5)
        lista = tk.Listbox(ventana, width=50); lista.pack()
        actualizar_lista(lista)

        estado_label = tk.Label(ventana, bg="#0f4c81", fg="white")
        estado_label.pack(pady=5)
        def actualizar_estado():
            estado_label.config(text=f"Espacio disponible: {parking.capacidad_actual()} / {parking.capacidad}")
        actualizar_estado()

    def mostrar_salida():
        limpiar_ventana()

        tk.Label(ventana, text="Registro de Salida", font=("Helvetica", 14, "bold"), bg="#0f4c81", fg="white").pack(pady=10)

        tk.Label(ventana, text="Placa del vehículo:", bg="#0f4c81", fg="white").pack()
        placa = tk.Entry(ventana); placa.pack()

        def registrar_salida():
            vehiculo = parking.registrar_salida(placa.get())
            if vehiculo:
                pago = parking.calcular_pago(vehiculo)
                messagebox.showinfo("Salida", f"Pago: S/ {pago}")
                actualizar_lista(lista)
                actualizar_estado()
            else:
                messagebox.showerror("Error", "Vehículo no encontrado")

        tk.Button(ventana, text="Registrar Salida", command=registrar_salida, bg="white").pack(pady=10)
        tk.Button(ventana, text="Volver al menú", command=mostrar_menu, bg="white").pack()

        # Lista de vehículos actuales
        tk.Label(ventana, text="Vehículos en Parking:", bg="#0f4c81", fg="white").pack(pady=5)
        lista = tk.Listbox(ventana, width=50); lista.pack()
        actualizar_lista(lista)

        estado_label = tk.Label(ventana, bg="#0f4c81", fg="white")
        estado_label.pack(pady=5)
        def actualizar_estado():
            estado_label.config(text=f"Espacio disponible: {parking.capacidad_actual()} / {parking.capacidad}")
        actualizar_estado()

    def actualizar_lista(listbox):
        listbox.delete(0, tk.END)
        for v in parking.obtener_vehiculos():
            listbox.insert(tk.END, f"{v.placa} - {v.marca} - {v.conductor.nombre}")

    def limpiar_ventana():
        for widget in ventana.winfo_children():
            widget.destroy()

    ventana.title("Tecsup Parking")
    ventana.geometry("420x600")
    ventana.configure(bg="#0f4c81")
    mostrar_menu()
    ventana.mainloop()
