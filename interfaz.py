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

        # Título principal
        tk.Label(ventana, text="Registro de Entrada", font=("Helvetica", 14, "bold"), bg="#0f4c81", fg="white").pack(pady=10)

        # Frame principal para el formulario
        form_frame = tk.Frame(ventana, bg="#0f4c81")
        form_frame.pack(padx=20, pady=5)

        # Etiquetas y campos alineados con grid
        etiquetas = ["Nombre:", "DNI:", "Placa:", "Marca:", "Color:"]
        entradas = []
        
        for i, texto in enumerate(etiquetas):
            tk.Label(form_frame, text=texto, bg="#0f4c81", fg="white", anchor="e").grid(row=i, column=0, sticky="e", padx=5, pady=3)
            entrada = tk.Entry(form_frame, width=25)
            entrada.grid(row=i, column=1, sticky="w", padx=5, pady=3)
            entradas.append(entrada)
        
        nombre, dni, placa, marca, color = entradas
        
        # Frame para el tipo de usuario
        tipo_frame = tk.Frame(form_frame, bg="#0f4c81")
        tipo_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        tk.Label(tipo_frame, text="Tipo:", bg="#0f4c81", fg="white").grid(row=0, column=0, padx=5)
        
        tipo_var = tk.StringVar(value="estudiante")
        tk.Radiobutton(tipo_frame, text="Estudiante", variable=tipo_var, value="estudiante", 
                    bg="#0f4c81", fg="white", selectcolor="#0f4c81").grid(row=0, column=1)
        tk.Radiobutton(tipo_frame, text="Profesor", variable=tipo_var, value="profesor",
                    bg="#0f4c81", fg="white", selectcolor="#0f4c81").grid(row=0, column=2)

        # Frame para botones
        buttons_frame = tk.Frame(ventana, bg="#0f4c81")
        buttons_frame.pack(pady=10)
        
        def registrar():
            conductor = Conductor(nombre.get(), dni.get(), tipo_var.get())
            vehiculo = Vehiculo(placa.get(), marca.get(), color.get(), conductor)
            if parking.registrar_ingreso(vehiculo):
                messagebox.showinfo("Éxito", "Vehículo ingresado")
                actualizar_lista(lista)
                actualizar_estado()
            else:
                messagebox.showerror("Error", "Parking lleno")

        tk.Button(buttons_frame, text="Registrar", command=registrar, bg="white", width=15).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(buttons_frame, text="Volver al menú", command=mostrar_menu, bg="white", width=15).grid(row=1, column=0, padx=5, pady=5)

        # Lista de vehículos
        tk.Label(ventana, text="Vehículos en Parking:", bg="#0f4c81", fg="white").pack(pady=5)
        lista = tk.Listbox(ventana, width=50, height=10)
        lista.pack(padx=20, pady=5)
        actualizar_lista(lista)

        # Estado del parking
        estado_label = tk.Label(ventana, bg="#0f4c81", fg="white")
        estado_label.pack(pady=5)
        
        def actualizar_estado():
            estado_label.config(text=f"Vehiculos en el parking: {parking.ocupados} / {parking.capacidad}")
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
            estado_label.config(text=f"Vehiculos en el parking: {parking.ocupados} / {parking.capacidad}")
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
