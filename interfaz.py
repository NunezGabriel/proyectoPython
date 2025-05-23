import tkinter as tk
from tkinter import ttk, messagebox
from vehiculo import Auto, Moto, Bicicleta
from conductor import Conductor
from parking import Parking

class TecsupParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tecsup Parking - Gestión Vehicular")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Configurar parking con capacidades diferentes
        self.parking = Parking(capacidad_autos=20, capacidad_motos=30, capacidad_bicis=50)
        
        # Estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=('Helvetica', 10))
        self.style.configure("TButton", font=('Helvetica', 10), padding=5)
        self.style.configure("Header.TLabel", font=('Helvetica', 14, 'bold'), foreground="#0f4c81")
        
        # Inicializar widgets que se actualizarán
        self.lbl_autos = None
        self.lbl_motos = None
        self.lbl_bicis = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de Menú Principal
        self.tab_menu = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_menu, text="Menú Principal")
        self.crear_menu_principal()
        
        # Pestaña para Autos
        self.tab_autos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_autos, text="Gestión de Autos")
        self.crear_formulario_vehiculo(self.tab_autos, "Auto")
        
        # Pestaña para Motos
        self.tab_motos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_motos, text="Gestión de Motos")
        self.crear_formulario_vehiculo(self.tab_motos, "Moto")
        
        # Pestaña para Bicicletas
        self.tab_bicis = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_bicis, text="Gestión de Bicicletas")
        self.crear_formulario_vehiculo(self.tab_bicis, "Bicicleta")
        
        # Pestaña de Reportes
        self.tab_reportes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reportes, text="Reportes")
        self.crear_tabla_reportes()
        
        # Mostrar primero el menú principal
        self.notebook.select(self.tab_menu)
    
    def crear_menu_principal(self):
        # Encabezado
        ttk.Label(self.tab_menu, text="Tecsup Parking", style="Header.TLabel").pack(pady=20)
        
        # Frame para estado del parking
        estado_frame = ttk.Frame(self.tab_menu)
        estado_frame.pack(pady=10)
        
        ttk.Label(estado_frame, text="Estado del Parking:", style="Header.TLabel").grid(row=0, columnspan=3)
        
        # Inicializar las etiquetas de estado
        self.lbl_autos = ttk.Label(estado_frame, text="Autos: -/-")
        self.lbl_autos.grid(row=1, column=0, padx=10)
        
        self.lbl_motos = ttk.Label(estado_frame, text="Motos: -/-")
        self.lbl_motos.grid(row=1, column=1, padx=10)
        
        self.lbl_bicis = ttk.Label(estado_frame, text="Bicicletas: -/-")
        self.lbl_bicis.grid(row=1, column=2, padx=10)
        
        # Actualizar estado con los valores reales
        self.actualizar_estado_parking()
        
        # Botones principales
        btn_frame = ttk.Frame(self.tab_menu)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Gestión de Autos", 
                  command=lambda: self.notebook.select(self.tab_autos)).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(btn_frame, text="Gestión de Motos", 
                  command=lambda: self.notebook.select(self.tab_motos)).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(btn_frame, text="Gestión de Bicicletas", 
                  command=lambda: self.notebook.select(self.tab_bicis)).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(btn_frame, text="Ver Reportes", 
                  command=lambda: self.notebook.select(self.tab_reportes)).grid(row=1, column=1, padx=10, pady=5)
    
    def crear_formulario_vehiculo(self, parent, tipo_vehiculo):
        # Frame principal con scroll
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido del formulario
        ttk.Label(scrollable_frame, text=f"Registro de {tipo_vehiculo}", style="Header.TLabel").grid(row=0, columnspan=2, pady=10)
        
        # Campos comunes
        ttk.Label(scrollable_frame, text="Nombre del Conductor:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_nombre = ttk.Entry(scrollable_frame)
        entry_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(scrollable_frame, text="DNI:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        entry_dni = ttk.Entry(scrollable_frame)
        entry_dni.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Tipo de usuario
        ttk.Label(scrollable_frame, text="Tipo de Usuario:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tipo_usuario = tk.StringVar(value="estudiante")
        
        ttk.Radiobutton(scrollable_frame, text="Estudiante", variable=tipo_usuario, value="estudiante").grid(row=3, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(scrollable_frame, text="Profesor", variable=tipo_usuario, value="profesor").grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        # Campos específicos del vehículo
        if tipo_vehiculo in ["Auto", "Moto"]:
            ttk.Label(scrollable_frame, text="Placa:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
            entry_placa = ttk.Entry(scrollable_frame)
            entry_placa.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(scrollable_frame, text="Marca:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        entry_marca = ttk.Entry(scrollable_frame)
        entry_marca.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(scrollable_frame, text="Color:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        entry_color = ttk.Entry(scrollable_frame)
        entry_color.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        
        if tipo_vehiculo == "Moto":
            ttk.Label(scrollable_frame, text="Cilindrada (cc):").grid(row=8, column=0, padx=5, pady=5, sticky="e")
            entry_cilindrada = ttk.Entry(scrollable_frame)
            entry_cilindrada.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        elif tipo_vehiculo == "Bicicleta":
            ttk.Label(scrollable_frame, text="Modelo:").grid(row=8, column=0, padx=5, pady=5, sticky="e")
            entry_modelo = ttk.Entry(scrollable_frame)
            entry_modelo.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        
        # Botones
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=9, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Registrar Entrada", 
                  command=lambda: self.registrar_entrada(
                      tipo_vehiculo,
                      entry_nombre.get(),
                      entry_dni.get(),
                      tipo_usuario.get(),
                      entry_placa.get() if tipo_vehiculo in ["Auto", "Moto"] else None,
                      entry_marca.get(),
                      entry_color.get(),
                      entry_cilindrada.get() if tipo_vehiculo == "Moto" else None,
                      entry_modelo.get() if tipo_vehiculo == "Bicicleta" else None
                  )).grid(row=0, column=0, padx=5)
        
        ttk.Button(btn_frame, text="Registrar Salida", 
                  command=lambda: self.registrar_salida(
                      entry_placa.get() if tipo_vehiculo in ["Auto", "Moto"] else "BIC-" + entry_dni.get()[-4:]
                  )).grid(row=0, column=1, padx=5)
        
        ttk.Button(btn_frame, text="Volver al Menú", 
                  command=lambda: self.notebook.select(self.tab_menu)).grid(row=0, column=2, padx=5)
        
        # Lista de vehículos
        ttk.Label(scrollable_frame, text="Vehículos Registrados:", style="Header.TLabel").grid(row=10, columnspan=2, pady=10)
        
        # Usamos un Treeview para mostrar la información en formato tabla
        columns = ("Placa", "Tipo", "Marca", "Color", "Conductor", "DNI", "Tipo Usuario")
        self.tree = ttk.Treeview(scrollable_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        
        self.tree.grid(row=11, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Actualizar la lista
        self.actualizar_lista_vehiculos()
    
    def crear_tabla_reportes(self):
        # Frame principal
        main_frame = ttk.Frame(self.tab_reportes)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(main_frame, text="Reporte de Vehículos", style="Header.TLabel").pack(pady=10)
        
        # Estado del parking
        estado_frame = ttk.Frame(main_frame)
        estado_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(estado_frame, text="Capacidad Actual:", style="Header.TLabel").grid(row=0, columnspan=3)
        
        self.lbl_autos = ttk.Label(estado_frame, text="Autos: -/-")
        self.lbl_autos.grid(row=1, column=0, padx=10)
        
        self.lbl_motos = ttk.Label(estado_frame, text="Motos: -/-")
        self.lbl_motos.grid(row=1, column=1, padx=10)
        
        self.lbl_bicis = ttk.Label(estado_frame, text="Bicicletas: -/-")
        self.lbl_bicis.grid(row=1, column=2, padx=10)
        
        # Tabla de vehículos
        columns = ("Placa", "Tipo", "Marca", "Color", "Conductor", "DNI", "Tipo Usuario", "Hora Entrada")
        self.tree_reportes = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree_reportes.heading(col, text=col)
            self.tree_reportes.column(col, width=120, anchor="center")
        
        self.tree_reportes.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botón de actualizar
        ttk.Button(main_frame, text="Actualizar Reportes", 
                  command=self.actualizar_reportes).pack(pady=10)
        
        # Botón de volver
        ttk.Button(main_frame, text="Volver al Menú", 
                  command=lambda: self.notebook.select(self.tab_menu)).pack()
        
        # Actualizar reportes inicial
        self.actualizar_reportes()
    
    def registrar_entrada(self, tipo_vehiculo, nombre, dni, tipo_usuario, placa, marca, color, cilindrada=None, modelo=None):
        # Validación de campos
        if not nombre or not dni:
            messagebox.showerror("Error", "Nombre y DNI son obligatorios")
            return
            
        if tipo_vehiculo in ["Auto", "Moto"] and not placa:
            messagebox.showerror("Error", "La placa es obligatoria para autos y motos")
            return
            
        conductor = Conductor(nombre, dni, tipo_usuario)
        
        try:
            if tipo_vehiculo == "Auto":
                vehiculo = Auto(placa, marca, color, conductor)
            elif tipo_vehiculo == "Moto":
                vehiculo = Moto(placa, marca, color, conductor, cilindrada)
            elif tipo_vehiculo == "Bicicleta":
                vehiculo = Bicicleta(marca, color, conductor, modelo)
            
            if self.parking.registrar_ingreso(vehiculo):
                messagebox.showinfo("Éxito", f"{tipo_vehiculo} registrado correctamente")
                self.actualizar_lista_vehiculos()
                self.actualizar_estado_parking()
            else:
                messagebox.showerror("Error", f"No hay espacio disponible para {tipo_vehiculo.lower()}s")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def registrar_salida(self, placa):
        vehiculo = self.parking.registrar_salida(placa)
        if vehiculo:
            pago = self.parking.calcular_pago(vehiculo)
            mensaje = f"Vehículo {vehiculo.placa} registrado como salida.\n"
            mensaje += f"Conductor: {vehiculo.conductor.nombre}\n"
            mensaje += f"Tiempo estacionado: {round((vehiculo.hora_salida - vehiculo.hora_entrada)/60, 2)} minutos\n"
            
            if pago > 0:
                mensaje += f"Total a pagar: S/ {pago:.2f}"
            else:
                mensaje += "No requiere pago (Profesor)"
                
            messagebox.showinfo("Salida Registrada", mensaje)
            self.actualizar_lista_vehiculos()
            self.actualizar_estado_parking()
            self.actualizar_reportes()
        else:
            messagebox.showerror("Error", "Vehículo no encontrado")
    
    def actualizar_lista_vehiculos(self):
        # Limpiar el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Agregar los vehículos actuales
        for vehiculo in self.parking.obtener_vehiculos():
            self.tree.insert("", "end", values=(
                vehiculo.placa,
                vehiculo.tipo_vehiculo,
                vehiculo.marca,
                vehiculo.color,
                vehiculo.conductor.nombre,
                vehiculo.conductor.dni,
                "Profesor" if vehiculo.conductor.tipo == "profesor" else "Estudiante"
            ))
    
    def actualizar_estado_parking(self):
        estado = self.parking.obtener_estado()
        self.lbl_autos.config(text=f"Autos: {estado['autos']}")
        self.lbl_motos.config(text=f"Motos: {estado['motos']}")
        self.lbl_bicis.config(text=f"Bicicletas: {estado['bicicletas']}")
    
    def actualizar_reportes(self):
        # Limpiar el treeview
        for item in self.tree_reportes.get_children():
            self.tree_reportes.delete(item)
            
        # Agregar los vehículos actuales con hora de entrada
        for vehiculo in self.parking.obtener_vehiculos():
            from datetime import datetime
            hora_entrada = datetime.fromtimestamp(vehiculo.hora_entrada).strftime('%H:%M:%S')
            
            self.tree_reportes.insert("", "end", values=(
                vehiculo.placa,
                vehiculo.tipo_vehiculo,
                vehiculo.marca,
                vehiculo.color,
                vehiculo.conductor.nombre,
                vehiculo.conductor.dni,
                "Profesor" if vehiculo.conductor.tipo == "profesor" else "Estudiante",
                hora_entrada
            ))
        
        # Actualizar estado del parking
        self.actualizar_estado_parking()

def lanzar_app():
    root = tk.Tk()
    app = TecsupParkingApp(root)
    root.mainloop()