import tkinter as tk
from tkinter import ttk, messagebox
from vehiculo import Auto, Moto, Bicicleta
from conductor import Conductor
from parking import Parking
from datetime import datetime

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

        # Configurar colores y estilos
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=('Helvetica', 10))
        self.style.configure("Header.TLabel", font=('Helvetica', 14, 'bold'), foreground="#37c8fa")

        # Configuración específica para botones
        self.style.configure("TButton", 
                        font=('Helvetica', 10),
                        padding=5,
                        background="#37c8fa",  # Color de fondo
                        foreground="white",    # Color del texto (blanco para mejor contraste)
                        borderwidth=1)

        # Cambiar el color cuando el botón está presionado
        self.style.map("TButton",
                    background=[('pressed', '#2aa8d9'),  # Un tono más oscuro al presionar
                                ('active', '#45d2ff')],   # Un tono más claro al pasar el mouse
                    foreground=[('pressed', 'white'),
                                ('active', 'white')])
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configurar el estilo para los headers del Treeview
        self.style.configure("Treeview.Heading",
                        background="#3e1ad9",  # Color morado para los headers
                        foreground="white",    # Texto blanco para mejor contraste
                        font=('Helvetica', 10, 'bold'),
                        padding=5,
                        relief="flat")        # Sin relieve para un look moderno

        # Configurar el hover para los headers
        self.style.map("Treeview.Heading",
                    background=[('active', '#5a36e0')],  # Color más claro al pasar el mouse
                    relief=[('active', 'groove')])       # Efecto al pasar el mouse
        
        # Configurar el estilo del Treeview en general
        self.style.configure("Treeview",
                        background="#ffffff",
                        foreground="#333333",
                        rowheight=25,
                        fieldbackground="#ffffff")

        # Alternar colores de filas para mejor legibilidad
        self.style.map("Treeview",
                    background=[('selected', '#3e1ad9')],  # Color selección
                    foreground=[('selected', 'white')])
                
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
        # Frame principal con nuevo diseño
        main_frame = ttk.Frame(self.tab_menu, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título principal
        ttk.Label(main_frame, 
                text="Tecsup Parking", 
                style="Header.TLabel",
                font=('Helvetica', 24, 'bold')).pack(pady=(0, 30))

        # Contenedor de cards
        cards_frame = ttk.Frame(main_frame)
        cards_frame.pack(fill=tk.BOTH, expand=True)

        # Estilo para las cards y etiquetas
        self.style.configure("Card.TFrame", 
                            background="#ffffff", 
                            relief="solid", 
                            borderwidth=1)

        self.style.configure("CardTitle.TLabel", 
                            background="#ffffff", 
                            font=('Helvetica', 13, 'bold'),
                            foreground="#333333")

        self.style.configure("CardDesc.TLabel", 
                            background="#ffffff", 
                            font=('Helvetica', 10),
                            foreground="#666666",
                            wraplength=180)

        self.style.configure("Card.TButton", 
                            background="#33ccff", 
                            foreground="white", 
                            font=('Helvetica', 10, 'bold'))

        # Datos de las cards
        cards_data = [
            ("Gestión de Autos", "Administra el ingreso y salida de autos del estacionamiento.",
            lambda: self.notebook.select(self.tab_autos)),
            ("Gestión de Motos", "Controla las motocicletas que ingresan y salen del recinto.",
            lambda: self.notebook.select(self.tab_motos)),
            ("Gestión de Bicicletas", "Gestiona el parqueo de bicicletas con registro y control.",
            lambda: self.notebook.select(self.tab_bicis)),
            ("Ver Reportes", "Consulta los reportes de uso del estacionamiento por tipo de vehículo.",
            lambda: self.notebook.select(self.tab_reportes))
        ]

        for i, (titulo, desc, comando) in enumerate(cards_data):
            card = ttk.Frame(cards_frame, style="Card.TFrame", width=200, height=160)
            card.grid(row=i//2, column=i%2, padx=15, pady=15, sticky="nsew")
            
            # Contenido dentro de la card
            inner = tk.Frame(card, bg="#ffffff")
            inner.pack(fill='both', expand=True, padx=10, pady=10)

            tk.Label(inner, text=titulo, font=('Helvetica', 12, 'bold'), bg="#ffffff", fg="#333333").pack(anchor="w")
            tk.Label(inner, text=desc, font=('Helvetica', 9), bg="#ffffff", fg="#777777", wraplength=180, justify='left').pack(anchor="w", pady=(5, 15))
            
            tk.Button(inner, text="Acceder", bg="#33ccff", fg="white", font=("Helvetica", 9, 'bold'),
                    relief='flat', cursor="hand2", command=comando).pack(anchor="e", pady=(10, 0))

        # Estado del parking
        estado_frame = ttk.Frame(main_frame)
        estado_frame.pack(pady=(30, 10))

        ttk.Label(estado_frame, 
                text=f"Autos: {self.parking.ocupados_autos}/{self.parking.capacidad_autos} | "
                    f"Motos: {self.parking.ocupados_motos}/{self.parking.capacidad_motos} | "
                    f"Bicicletas: {self.parking.ocupados_bicis}/{self.parking.capacidad_bicis}",
                font=('Helvetica', 10)).pack()

        # Configurar grid para expansión uniforme
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_rowconfigure(1, weight=1)

             
    def crear_formulario_vehiculo(self, parent, tipo_vehiculo):
        # Configurar estilos para el formulario
        self.style.configure("Form.TFrame", background="#f5f5f5", padding=10)
        self.style.configure("FormHeader.TLabel", font=('Helvetica', 18, 'bold'), foreground="#333333")
        self.style.configure("FormLabel.TLabel", font=('Helvetica', 10), foreground="#555555")
        self.style.configure("FormEntry.TEntry", font=('Helvetica', 10), padding=5)
        self.style.configure("FormButton.TButton", font=('Helvetica', 10, 'bold'), padding=6)
        self.style.configure("FormRadio.TRadiobutton", font=('Helvetica', 10), padding=5)
        
        # Frame principal con scroll
        main_frame = ttk.Frame(parent, style="Form.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Contenedor con borde y padding
        container = ttk.Frame(main_frame, style="Card.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(container, highlightthickness=0, bg="#ffffff")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Card.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Contenido del formulario - Sección de Registro
        form_frame = ttk.Frame(scrollable_frame, style="Card.TFrame", padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título del formulario
        ttk.Label(form_frame, 
                text=f"Registro de {tipo_vehiculo}", 
                style="FormHeader.TLabel").grid(row=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Campos del formulario
        row_counter = 1
        
        # Nombre del Conductor
        ttk.Label(form_frame, text="Nombre del Conductor:", style="FormLabel.TLabel").grid(
            row=row_counter, column=0, padx=10, pady=8, sticky="e")
        entry_nombre = ttk.Entry(form_frame, style="FormEntry.TEntry", width=30)
        entry_nombre.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
        row_counter += 1
        
        # DNI
        ttk.Label(form_frame, text="DNI:", style="FormLabel.TLabel").grid(
            row=row_counter, column=0, padx=10, pady=8, sticky="e")
        entry_dni = ttk.Entry(form_frame, style="FormEntry.TEntry", width=20)
        entry_dni.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
        row_counter += 1
        
        # Tipo de Usuario
        ttk.Label(form_frame, text="Tipo de Usuario:", style="FormLabel.TLabel").grid(
            row=row_counter, column=0, padx=10, pady=8, sticky="e")
        
        user_type_frame = ttk.Frame(form_frame, style="Card.TFrame")
        user_type_frame.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
        
        tipo_usuario = tk.StringVar(value="estudiante")
        ttk.Radiobutton(user_type_frame, text="Estudiante", variable=tipo_usuario, 
                    value="estudiante", style="FormRadio.TRadiobutton").pack(side="left")
        ttk.Radiobutton(user_type_frame, text="Profesor", variable=tipo_usuario, 
                    value="profesor", style="FormRadio.TRadiobutton").pack(side="left", padx=10)
        row_counter += 1
        
        # Campos específicos del vehículo
        if tipo_vehiculo in ["Auto", "Moto"]:
            ttk.Label(form_frame, text="Placa:", style="FormLabel.TLabel").grid(
                row=row_counter, column=0, padx=10, pady=8, sticky="e")
            entry_placa = ttk.Entry(form_frame, style="FormEntry.TEntry", width=15)
            entry_placa.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
            row_counter += 1
        
        # Marca
        ttk.Label(form_frame, text="Marca:", style="FormLabel.TLabel").grid(
            row=row_counter, column=0, padx=10, pady=8, sticky="e")
        entry_marca = ttk.Entry(form_frame, style="FormEntry.TEntry", width=20)
        entry_marca.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
        row_counter += 1
        
        # Color
        ttk.Label(form_frame, text="Color:", style="FormLabel.TLabel").grid(
            row=row_counter, column=0, padx=10, pady=8, sticky="e")
        entry_color = ttk.Entry(form_frame, style="FormEntry.TEntry", width=15)
        entry_color.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
        row_counter += 1
        
        # Campos adicionales según tipo de vehículo
        if tipo_vehiculo == "Moto":
            ttk.Label(form_frame, text="Cilindrada (cc):", style="FormLabel.TLabel").grid(
                row=row_counter, column=0, padx=10, pady=8, sticky="e")
            entry_cilindrada = ttk.Entry(form_frame, style="FormEntry.TEntry", width=10)
            entry_cilindrada.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
            row_counter += 1
        elif tipo_vehiculo == "Bicicleta":
            ttk.Label(form_frame, text="Modelo:", style="FormLabel.TLabel").grid(
                row=row_counter, column=0, padx=10, pady=8, sticky="e")
            entry_modelo = ttk.Entry(form_frame, style="FormEntry.TEntry", width=20)
            entry_modelo.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
            row_counter += 1
        
        # Botones de acción
        btn_frame = ttk.Frame(form_frame, style="Card.TFrame")
        btn_frame.grid(row=row_counter, columnspan=2, pady=(20, 10), sticky="e")
        
        ttk.Button(btn_frame, text="Volver al Menú", style="FormButton.TButton",
                command=lambda: self.notebook.select(self.tab_menu)).pack(side="right", padx=5)
        
        ttk.Button(btn_frame, text="Registrar Salida", style="FormButton.TButton",
                command=lambda: self.registrar_salida(
                    entry_placa.get() if tipo_vehiculo in ["Auto", "Moto"] else "BIC-" + entry_dni.get()[-4:]
                )).pack(side="right", padx=5)
        
        ttk.Button(btn_frame, text="Registrar Entrada", style="FormButton.TButton",
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
                )).pack(side="right", padx=5)
        
        # Sección de listado de vehículos
        list_frame = ttk.Frame(scrollable_frame, style="Card.TFrame", padding=20)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        ttk.Label(list_frame, 
                text="Vehículos Registrados", 
                style="FormHeader.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Configurar Treeview según tipo de vehículo
        tree_style = ttk.Style()
        tree_style.configure("Treeview", font=('Helvetica', 10), rowheight=25)
        tree_style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        if tipo_vehiculo == "Auto":
            self.tree_autos = ttk.Treeview(list_frame, 
                                        columns=("Placa", "Marca", "Color", "Conductor", "DNI", "Tipo"), 
                                        show="headings", height=8, style="Treeview")
            for col in ["Placa", "Marca", "Color", "Conductor", "DNI", "Tipo"]:
                self.tree_autos.heading(col, text=col)
                self.tree_autos.column(col, width=120, anchor="center")
            self.tree_autos.pack(fill=tk.BOTH, expand=True)
            
        elif tipo_vehiculo == "Moto":
            self.tree_motos = ttk.Treeview(list_frame, 
                                        columns=("Placa", "Marca", "Color", "Conductor", "DNI", "Tipo", "Cilindrada"), 
                                        show="headings", height=8, style="Treeview")
            for col in ["Placa", "Marca", "Color", "Conductor", "DNI", "Tipo", "Cilindrada"]:
                self.tree_motos.heading(col, text=col)
                self.tree_motos.column(col, width=110, anchor="center")
            self.tree_motos.pack(fill=tk.BOTH, expand=True)
            
        elif tipo_vehiculo == "Bicicleta":
            self.tree_bicis = ttk.Treeview(list_frame, 
                                        columns=("ID", "Marca", "Color", "Conductor", "DNI", "Tipo", "Modelo"), 
                                        show="headings", height=8, style="Treeview")
            for col in ["ID", "Marca", "Color", "Conductor", "DNI", "Tipo", "Modelo"]:
                self.tree_bicis.heading(col, text=col)
                self.tree_bicis.column(col, width=110, anchor="center")
            self.tree_bicis.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid para expansión uniforme
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=3)
    
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
            
        try:
            conductor = Conductor(nombre, dni, tipo_usuario)
            
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
                self.actualizar_reportes()
                # Forzar actualización de la interfaz
                self.root.update_idletasks()
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
        # Obtener todos los Treeviews
        trees = {
            "Auto": getattr(self, "tree_autos", None),
            "Moto": getattr(self, "tree_motos", None),
            "Bicicleta": getattr(self, "tree_bicis", None),
            "Reportes": getattr(self, "tree_reportes", None)
        }
        
        # Limpiar todos los Treeviews
        for tree in trees.values():
            if tree:
                for item in tree.get_children():
                    tree.delete(item)
        
        # Insertar vehículos en los Treeviews correspondientes
        for vehiculo in self.parking.obtener_vehiculos():
            datos_base = (
                vehiculo.placa if hasattr(vehiculo, "placa") else f"BIC-{vehiculo.conductor.dni[-4:]}",
                vehiculo.marca,
                vehiculo.color,
                vehiculo.conductor.nombre,
                vehiculo.conductor.dni,
                "Profesor" if vehiculo.conductor.tipo == "profesor" else "Estudiante"
            )
            
            if vehiculo.tipo_vehiculo == "Auto" and trees["Auto"]:
                trees["Auto"].insert("", "end", values=datos_base)
                
            elif vehiculo.tipo_vehiculo == "Moto" and trees["Moto"]:
                datos_moto = datos_base + (vehiculo.cilindrada,)
                trees["Moto"].insert("", "end", values=datos_moto)
                
            elif vehiculo.tipo_vehiculo == "Bicicleta" and trees["Bicicleta"]:
                datos_bici = (f"BIC-{vehiculo.conductor.dni[-4:]}",) + datos_base[1:] + (vehiculo.modelo,)
                trees["Bicicleta"].insert("", "end", values=datos_bici)
            
            # Insertar en reportes
            if trees["Reportes"]:
                hora_entrada = datetime.fromtimestamp(vehiculo.hora_entrada).strftime("%H:%M:%S") if vehiculo.hora_entrada else "N/A"
                trees["Reportes"].insert("", "end", values=(vehiculo.tipo_vehiculo,) + datos_base + (hora_entrada,))
    
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