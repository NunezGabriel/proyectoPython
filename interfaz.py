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

    def filtrar_por_conductor(self, tipo_vehiculo, nombre_buscar):
        """Filtra la tabla por nombre del conductor"""
        # Obtener el tree correspondiente
        if tipo_vehiculo == "Auto":
            tree = self.tree_autos
        elif tipo_vehiculo == "Moto":
            tree = self.tree_motos
        elif tipo_vehiculo == "Bicicleta":
            tree = self.tree_bicis
        else:
            return

        # Limpiar la tabla
        for item in tree.get_children():
            tree.delete(item)

        # Obtener todos los vehículos del tipo correspondiente
        vehiculos_filtrados = [v for v in self.parking.obtener_vehiculos() 
                             if v.tipo_vehiculo == tipo_vehiculo]

        # Si hay texto de búsqueda, filtrar por nombre del conductor
        if nombre_buscar.strip():
            vehiculos_filtrados = [v for v in vehiculos_filtrados 
                                 if nombre_buscar.lower() in v.conductor.nombre.lower()]

        # Mostrar vehículos filtrados
        for vehiculo in vehiculos_filtrados:
            datos_base = (
                vehiculo.placa if hasattr(vehiculo, "placa") else f"BIC-{vehiculo.conductor.dni[-4:]}",
                vehiculo.marca,
                vehiculo.color,
                vehiculo.conductor.nombre,
                vehiculo.conductor.dni,
                "Profesor" if vehiculo.conductor.tipo == "profesor" else "Estudiante"
            )
            
            if tipo_vehiculo == "Auto":
                tree.insert("", "end", values=datos_base)
            elif tipo_vehiculo == "Moto":
                datos_moto = datos_base + (vehiculo.cilindrada,)
                tree.insert("", "end", values=datos_moto)
            elif tipo_vehiculo == "Bicicleta":
                datos_bici = (f"BIC-{vehiculo.conductor.dni[-4:]}",) + datos_base[1:] + (vehiculo.modelo,)
                tree.insert("", "end", values=datos_bici)
             
    def crear_formulario_vehiculo(self, parent, tipo_vehiculo):
        # Configurar estilos para el formulario
        self.style.configure("Form.TFrame", background="#f5f5f5", padding=10)
        self.style.configure("FormHeader.TLabel", font=('Helvetica', 18, 'bold'), foreground="#333333")
        self.style.configure("FormLabel.TLabel", font=('Helvetica', 10), foreground="#555555")
        self.style.configure("FormEntry.TEntry", font=('Helvetica', 10), padding=5)
        self.style.configure("FormButton.TButton", font=('Helvetica', 10, 'bold'), padding=6)
        self.style.configure("FormRadio.TRadiobutton", font=('Helvetica', 10), padding=5)
        
        # Frame principal sin scroll (para permitir crecimiento automático)
        main_frame = ttk.Frame(parent, style="Form.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurar tamaño de la ventana principal (esto debe hacerse en la ventana raíz, no en el Notebook)
        root = parent.winfo_toplevel()  # Obtenemos la ventana principal
        root.minsize(900, 600)  # Tamaño mínimo inicial
        root.geometry("1000x650")  # Tamaño inicial recomendado

        # Contenedor principal con dos columnas
        container = ttk.Frame(main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda - Formulario
        form_container = ttk.Frame(container, style="Card.TFrame", padding=20)
        form_container.pack(side="left", fill="y", padx=(0, 20), pady=10)
            
        # Título del formulario
        ttk.Label(form_container, 
                text=f"Registro de {tipo_vehiculo}", 
                style="FormHeader.TLabel").pack(anchor="w", pady=(0, 20))
        
        # Campos del formulario
        fields_frame = ttk.Frame(form_container)
        fields_frame.pack(fill="x")
        
        row_counter = 0
        
        # Nombre del Conductor
        ttk.Label(fields_frame, text="Nombre del Conductor:", style="FormLabel.TLabel").grid(
            row=row_counter, column=0, padx=10, pady=8, sticky="e")
        entry_nombre = ttk.Entry(fields_frame, style="FormEntry.TEntry", width=30)
        entry_nombre.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
        row_counter += 1
        
        # DNI
        ttk.Label(fields_frame, text="DNI:", style="FormLabel.TLabel").grid(
            row=row_counter, column=0, padx=10, pady=8, sticky="e")
        entry_dni = ttk.Entry(fields_frame, style="FormEntry.TEntry", width=20)
        entry_dni.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
        row_counter += 1
        
        # Tipo de Usuario
        ttk.Label(fields_frame, text="Tipo de Usuario:", style="FormLabel.TLabel").grid(
            row=row_counter, column=0, padx=10, pady=8, sticky="e")
        
        user_type_frame = ttk.Frame(fields_frame)
        user_type_frame.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
        
        tipo_usuario = tk.StringVar(value="estudiante")
        ttk.Radiobutton(user_type_frame, text="Estudiante", variable=tipo_usuario, 
                    value="estudiante", style="FormRadio.TRadiobutton").pack(side="left")
        ttk.Radiobutton(user_type_frame, text="Profesor", variable=tipo_usuario, 
                    value="profesor", style="FormRadio.TRadiobutton").pack(side="left", padx=10)
        row_counter += 1
        
        # Campos específicos del vehículo
        if tipo_vehiculo in ["Auto", "Moto"]:
            ttk.Label(fields_frame, text="Placa:", style="FormLabel.TLabel").grid(
                row=row_counter, column=0, padx=10, pady=8, sticky="e")
            entry_placa = ttk.Entry(fields_frame, style="FormEntry.TEntry", width=15)
            entry_placa.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
            row_counter += 1
        
        # Marca
        ttk.Label(fields_frame, text="Marca:", style="FormLabel.TLabel").grid(
            row=row_counter, column=0, padx=10, pady=8, sticky="e")
        entry_marca = ttk.Entry(fields_frame, style="FormEntry.TEntry", width=20)
        entry_marca.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
        row_counter += 1
        
        # Color
        ttk.Label(fields_frame, text="Color:", style="FormLabel.TLabel").grid(
            row=row_counter, column=0, padx=10, pady=8, sticky="e")
        entry_color = ttk.Entry(fields_frame, style="FormEntry.TEntry", width=15)
        entry_color.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
        row_counter += 1
        
        # Campos adicionales según tipo de vehículo
        if tipo_vehiculo == "Moto":
            ttk.Label(fields_frame, text="Cilindrada (cc):", style="FormLabel.TLabel").grid(
                row=row_counter, column=0, padx=10, pady=8, sticky="e")
            entry_cilindrada = ttk.Entry(fields_frame, style="FormEntry.TEntry", width=10)
            entry_cilindrada.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
            row_counter += 1
        elif tipo_vehiculo == "Bicicleta":
            ttk.Label(fields_frame, text="Modelo:", style="FormLabel.TLabel").grid(
                row=row_counter, column=0, padx=10, pady=8, sticky="e")
            entry_modelo = ttk.Entry(fields_frame, style="FormEntry.TEntry", width=20)
            entry_modelo.grid(row=row_counter, column=1, padx=10, pady=8, sticky="w")
            row_counter += 1
        
        # Columna derecha - Tabla y botones
        table_container = ttk.Frame(container, style="Card.TFrame", padding=20)
        table_container.pack(side="left", fill="both", expand=True, pady=10)
        
        # Frame para buscador y botones
        search_btn_frame = ttk.Frame(table_container)
        search_btn_frame.pack(fill="x", pady=(0, 15))
        
        # Buscador
        search_frame = ttk.Frame(search_btn_frame)
        search_frame.pack(side="left", fill="x", expand=True)
        
        ttk.Label(search_frame, text="🔍 Buscar por conductor:", 
                 style="FormLabel.TLabel").pack(side="left", padx=(0, 5))
        entry_buscar = ttk.Entry(search_frame, style="FormEntry.TEntry", width=25)
        entry_buscar.pack(side="left", padx=(0, 10))
        
        # Función para buscar en tiempo real
        def on_search_change(*args):
            self.filtrar_por_conductor(tipo_vehiculo, entry_buscar.get())
        
        # Vincular la búsqueda al cambio de texto
        entry_buscar.bind('<KeyRelease>', on_search_change)
        
        # Botones de acción
        btn_frame = ttk.Frame(search_btn_frame)
        btn_frame.pack(side="right")
        
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
                )).pack(side="left", padx=2)
        
        ttk.Button(btn_frame, text="Registrar Salida", style="FormButton.TButton",
                command=lambda: self.registrar_salida(
                    entry_placa.get() if tipo_vehiculo in ["Auto", "Moto"] else "BIC-" + entry_dni.get()[-4:]
                )).pack(side="left", padx=2)
        
        ttk.Button(btn_frame, text="Volver al Menú", style="FormButton.TButton",
                command=lambda: self.notebook.select(self.tab_menu)).pack(side="left", padx=2)
        
        # Tabla de vehículos registrados
        ttk.Label(table_container, 
                text="Vehículos Registrados", 
                style="FormHeader.TLabel").pack(anchor="w", pady=(0, 10))
        
        # Configurar Treeview según tipo de vehículo
        tree_style = ttk.Style()
        tree_style.configure("Treeview", font=('Helvetica', 10), rowheight=25)
        tree_style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Frame para la tabla con scroll
        tree_frame = ttk.Frame(table_container)
        tree_frame.pack(fill="both", expand=True)
        
        # Scrollbar vertical
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side="right", fill="y")

        # Función para manejar la selección de fila en la tabla
        def on_row_select(event):
            # Obtener el Treeview correspondiente
            tree = None
            if tipo_vehiculo == "Auto":
                tree = self.tree_autos
            elif tipo_vehiculo == "Moto":
                tree = self.tree_motos
            elif tipo_vehiculo == "Bicicleta":
                tree = self.tree_bicis
            
            # Obtener el item seleccionado
            selected_item = tree.selection()
            if not selected_item:
                return
                
            item_data = tree.item(selected_item, 'values')
            
            # Rellenar formulario con los datos de la fila seleccionada
            if tipo_vehiculo in ["Auto", "Moto"]:
                entry_placa.delete(0, tk.END)
                entry_placa.insert(0, item_data[0])  # Placa
                entry_marca.delete(0, tk.END)
                entry_marca.insert(0, item_data[1])  # Marca
                entry_color.delete(0, tk.END)
                entry_color.insert(0, item_data[2])  # Color
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, item_data[3])  # Conductor
                entry_dni.delete(0, tk.END)
                entry_dni.insert(0, item_data[4])  # DNI
                tipo_usuario.set("profesor" if item_data[5].lower() == "profesor" else "estudiante")  # Tipo usuario
                
                if tipo_vehiculo == "Moto":
                    entry_cilindrada.delete(0, tk.END)
                    if len(item_data) > 6:  # Asegurarse que hay cilindrada
                        entry_cilindrada.insert(0, item_data[6])  # Cilindrada
                    
            elif tipo_vehiculo == "Bicicleta":
                entry_marca.delete(0, tk.END)
                entry_marca.insert(0, item_data[1])  # Marca
                entry_color.delete(0, tk.END)
                entry_color.insert(0, item_data[2])  # Color
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, item_data[3])  # Conductor
                entry_dni.delete(0, tk.END)
                entry_dni.insert(0, item_data[4])  # DNI
                tipo_usuario.set("profesor" if item_data[5].lower() == "profesor" else "estudiante")  # Tipo usuario
                entry_modelo.delete(0, tk.END)
                if len(item_data) > 6:  # Asegurarse que hay modelo
                    entry_modelo.insert(0, item_data[6])  # Modelo        
        
        # Configurar Treeview según tipo de vehículo
        if tipo_vehiculo == "Auto":
            self.tree_autos = ttk.Treeview(tree_frame, 
                                        columns=("Placa", "Marca", "Color", "Conductor", "DNI", "Tipo"), 
                                        show="headings", height=12, style="Treeview", yscrollcommand=vsb.set)
            for col in ["Placa", "Marca", "Color", "Conductor", "DNI", "Tipo"]:
                self.tree_autos.heading(col, text=col)
                self.tree_autos.column(col, width=120, anchor="center")
            self.tree_autos.pack(fill="both", expand=True)
            self.tree_autos.bind("<ButtonRelease-1>", on_row_select)  # <-- Aquí el binding
            
        elif tipo_vehiculo == "Moto":
            self.tree_motos = ttk.Treeview(tree_frame, 
                                        columns=("Placa", "Marca", "Color", "Conductor", "DNI", "Tipo", "Cilindrada"), 
                                        show="headings", height=12, style="Treeview", yscrollcommand=vsb.set)
            for col in ["Placa", "Marca", "Color", "Conductor", "DNI", "Tipo", "Cilindrada"]:
                self.tree_motos.heading(col, text=col)
                self.tree_motos.column(col, width=110, anchor="center")
            self.tree_motos.pack(fill="both", expand=True)
            self.tree_motos.bind("<ButtonRelease-1>", on_row_select)  # <-- Aquí el binding
            
        elif tipo_vehiculo == "Bicicleta":
            self.tree_bicis = ttk.Treeview(tree_frame, 
                                        columns=("ID", "Marca", "Color", "Conductor", "DNI", "Tipo", "Modelo"), 
                                        show="headings", height=12, style="Treeview", yscrollcommand=vsb.set)
            for col in ["ID", "Marca", "Color", "Conductor", "DNI", "Tipo", "Modelo"]:
                self.tree_bicis.heading(col, text=col)
                self.tree_bicis.column(col, width=110, anchor="center")
            self.tree_bicis.pack(fill="both", expand=True)
            self.tree_bicis.bind("<ButtonRelease-1>", on_row_select)  # <-- Aquí el binding
        
        vsb.config(command=self.tree_autos.yview if tipo_vehiculo == "Auto" else 
                self.tree_motos.yview if tipo_vehiculo == "Moto" else 
                self.tree_bicis.yview)
        
        # Configurar expansión de la ventana
        root = parent.winfo_toplevel()  # Obtenemos la ventana principal
        root.minsize(1500, 800)  # Tamaño mínimo inicial
        root.geometry("1000x650")  # Tamaño inicial recomendado
    
    def crear_tabla_reportes(self):
        # Frame principal con nuevo estilo
        main_frame = ttk.Frame(self.tab_reportes, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título principal con nuevo estilo
        ttk.Label(main_frame, 
                text="Reporte de Vehículos", 
                style="Header.TLabel",
                font=('Helvetica', 18, 'bold')).pack(pady=(0, 15))
        
        # Panel de estado con nuevo diseño
        estado_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=10)
        estado_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(estado_frame, 
                text="Capacidad Actual", 
                style="FormHeader.TLabel",
                font=('Helvetica', 12, 'bold')).pack(anchor="w")
        
        # Contenedor para los indicadores
        indicators_frame = ttk.Frame(estado_frame)
        indicators_frame.pack(fill=tk.X, pady=5)
        
        # Estilo para los indicadores
        self.style.configure("Indicator.TLabel", 
                            font=('Helvetica', 10, 'bold'),
                            padding=5)
        
        # Indicador para Autos
        auto_frame = ttk.Frame(indicators_frame, style="Card.TFrame", padding=5)
        auto_frame.pack(side="left", padx=5, pady=5, fill=tk.X, expand=True)
        ttk.Label(auto_frame, text="🚗 Autos", style="Indicator.TLabel").pack()
        self.lbl_autos = ttk.Label(auto_frame, 
                                text="0/20", 
                                font=('Helvetica', 12),
                                foreground="#333333")
        self.lbl_autos.pack()
        
        # Indicador para Motos
        moto_frame = ttk.Frame(indicators_frame, style="Card.TFrame", padding=5)
        moto_frame.pack(side="left", padx=5, pady=5, fill=tk.X, expand=True)
        ttk.Label(moto_frame, text="🏍️ Motos", style="Indicator.TLabel").pack()
        self.lbl_motos = ttk.Label(moto_frame, 
                                text="0/30", 
                                font=('Helvetica', 12),
                                foreground="#333333")
        self.lbl_motos.pack()
        
        # Indicador para Bicicletas
        bici_frame = ttk.Frame(indicators_frame, style="Card.TFrame", padding=5)
        bici_frame.pack(side="left", padx=5, pady=5, fill=tk.X, expand=True)
        ttk.Label(bici_frame, text="🚲 Bicicletas", style="Indicator.TLabel").pack()
        self.lbl_bicis = ttk.Label(bici_frame, 
                                text="0/50", 
                                font=('Helvetica', 12),
                                foreground="#333333")
        self.lbl_bicis.pack()
        
        # Configurar estilo para la tabla
        self.style.configure("Treeview",
                            background="#ffffff",
                            foreground="#333333",
                            rowheight=28,
                            fieldbackground="#ffffff",
                            borderwidth=0)
        
        self.style.configure("Treeview.Heading",
                            background="#3e1ad9",
                            foreground="white",
                            font=('Helvetica', 10, 'bold'),
                            padding=5,
                            relief="flat")
        
        self.style.map("Treeview.Heading",
                    background=[('active', '#5a36e0')])
        
        self.style.map("Treeview",
                    background=[('selected', '#3e1ad9')],
                    foreground=[('selected', 'white')])
        
        # Frame para la tabla con scroll
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")
        
        # Configurar Treeview
        columns = ("Placa", "Tipo", "Marca", "Color", "Conductor", "DNI", "Tipo Usuario", "Hora Entrada")
        self.tree_reportes = ttk.Treeview(table_frame, 
                                        columns=columns, 
                                        show="headings", 
                                        height=12,
                                        style="Treeview",
                                        yscrollcommand=vsb.set,
                                        xscrollcommand=hsb.set)
        
        # Configurar columnas
        col_widths = {
            "Placa": 100,
            "Tipo": 80,
            "Marca": 100,
            "Color": 80,
            "Conductor": 120,
            "DNI": 100,
            "Tipo Usuario": 100,
            "Hora Entrada": 100
        }
        
        for col in columns:
            self.tree_reportes.heading(col, text=col)
            self.tree_reportes.column(col, width=col_widths.get(col, 100), anchor="center")
        
        # Empacar scrollbars y tabla
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree_reportes.pack(side="left", fill="both", expand=True)
        
        vsb.config(command=self.tree_reportes.yview)
        hsb.config(command=self.tree_reportes.xview)
        
        # Panel de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Botón de actualizar con nuevo estilo
        ttk.Button(button_frame, 
                text="🔄 Actualizar Reportes", 
                style="Accent.TButton",
                command=self.actualizar_reportes).pack(side="left", padx=5)
        
        # Botón de volver con nuevo estilo
        ttk.Button(button_frame, 
                text="← Volver al Menú", 
                style="TButton",
                command=lambda: self.notebook.select(self.tab_menu)).pack(side="right", padx=5)
        
        # Configurar estilos adicionales para los botones
        self.style.configure("Accent.TButton",
                            background="#3e1ad9",
                            foreground="white",
                            font=('Helvetica', 10, 'bold'),
                            padding=8)
        
        self.style.map("Accent.TButton",
                    background=[('active', '#5a36e0'), ('pressed', '#2a0d9c')])
        
        # Actualizar reportes inicial
        self.actualizar_reportes()

    def limpiar_formulario(self, tipo_vehiculo, entry_nombre, entry_dni, tipo_usuario, entry_placa, entry_marca, entry_color, entry_cilindrada=None, entry_modelo=None):
        """Limpia todos los campos del formulario"""
        entry_nombre.delete(0, tk.END)
        entry_dni.delete(0, tk.END)
        entry_marca.delete(0, tk.END)
        entry_color.delete(0, tk.END)
        tipo_usuario.set("estudiante")  # Valor por defecto
        
        if tipo_vehiculo in ["Auto", "Moto"] and entry_placa:
            entry_placa.delete(0, tk.END)
        
        if tipo_vehiculo == "Moto" and entry_cilindrada:
            entry_cilindrada.delete(0, tk.END)
        
        if tipo_vehiculo == "Bicicleta" and entry_modelo:
            entry_modelo.delete(0, tk.END)
    
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
                
                # Limpiar formulario después del registro exitoso
                self.limpiar_formulario_actual(tipo_vehiculo)
                
                # Forzar actualización de la interfaz
                self.root.update_idletasks()
            else:
                messagebox.showerror("Error", f"No hay espacio disponible para {tipo_vehiculo.lower()}s")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        
    def registrar_salida(self, placa):
        # Si no se proporciona placa (campo vacío), verificar si hay selección en el Treeview
        if not placa or placa.strip() == "":
            # Determinar qué Treeview está activo según la pestaña actual
            current_tab = self.notebook.tab(self.notebook.select(), "text")
            
            try:
                if current_tab == "Gestión de Autos" and self.tree_autos.selection():
                    selected_item = self.tree_autos.selection()[0]
                    placa = self.tree_autos.item(selected_item, 'values')[0]
                elif current_tab == "Gestión de Motos" and self.tree_motos.selection():
                    selected_item = self.tree_motos.selection()[0]
                    placa = self.tree_motos.item(selected_item, 'values')[0]
                elif current_tab == "Gestión de Bicicletas" and self.tree_bicis.selection():
                    selected_item = self.tree_bicis.selection()[0]
                    placa = self.tree_bicis.item(selected_item, 'values')[0]
            except:
                pass
        
        if not placa or placa.strip() == "":
            messagebox.showerror("Error", "No se ha seleccionado ningún vehículo")
            return
        
        vehiculo = self.parking.registrar_salida(placa)
        if vehiculo:
            pago = self.parking.calcular_pago(vehiculo)
            mensaje = f"Vehículo {vehiculo.placa if hasattr(vehiculo, 'placa') else 'BIC-' + vehiculo.conductor.dni[-4:]} registrado como salida.\n"
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
            
            # Limpiar formulario después del registro de salida exitoso
            current_tab = self.notebook.tab(self.notebook.select(), "text")
            if current_tab == "Gestión de Autos":
                self.limpiar_formulario_actual("Auto")
            elif current_tab == "Gestión de Motos":
                self.limpiar_formulario_actual("Moto")
            elif current_tab == "Gestión de Bicicletas":
                self.limpiar_formulario_actual("Bicicleta")
        else:
            messagebox.showerror("Error", "Vehículo no encontrado")
            
    def limpiar_formulario_actual(self, tipo_vehiculo):
        """Limpia el formulario de la pestaña activa"""
        # Obtener referencias a los widgets del formulario activo
        if tipo_vehiculo == "Auto":
            tab = self.tab_autos
        elif tipo_vehiculo == "Moto":
            tab = self.tab_motos
        elif tipo_vehiculo == "Bicicleta":
            tab = self.tab_bicis
        else:
            return
        
        # Buscar y limpiar todos los Entry widgets en la pestaña
        for widget in tab.winfo_children():
            self._limpiar_entries_recursivo(widget)

    def _limpiar_entries_recursivo(self, widget):
        """Función auxiliar para limpiar Entry widgets recursivamente"""
        if isinstance(widget, ttk.Entry):
            widget.delete(0, tk.END)
        elif hasattr(widget, 'winfo_children'):
            for child in widget.winfo_children():
                self._limpiar_entries_recursivo(child)
        
        # También limpiar radiobuttons
        if hasattr(widget, 'winfo_children'):
            for child in widget.winfo_children():
                if isinstance(child, ttk.Frame):
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.StringVar):
                            try:
                                subchild.set("estudiante")
                            except:
                                pass

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