import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constantes import FONDO_GENERAL
import mysql.connector

def obtener_datos_departamentos():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        cursor.execute("SELECT id, nombre, status FROM Departamentos")
        datos = cursor.fetchall()
        return datos if datos else [] 
    finally:
        con.close()

def obtener_datos_administradores():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        cursor.execute("""
            SELECT 
                u.id, 
                u.nombre, 
                u.apellido_paterno, 
                u.apellido_materno, 
                u.correo, 
                u.telefono, 
                d.nombre AS departamento, 
                u.status
            FROM 
                Usuarios u
            INNER JOIN Administradores a ON u.id = a.id_usuario
            INNER JOIN Departamentos d ON a.id_departamento = d.id
            WHERE 
                u.id_tipo_usuario = 1
        """)
        datos = cursor.fetchall()
        return datos if datos else []
    finally:
        con.close()


def iniciar_modulo_administradores(frame_contenido):
    # Limpia el contenido anterior si es necesario
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    # Y luego llama a la pantalla principal en ese frame
    mostrar_pantalla_principal(frame_contenido)

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def insertar_administrador(nombre, apellido_paterno, apellido_materno, correo, telefono, usuario, password, id_departamento, status, frame):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()

        # Paso 1: Insertar en Usuarios
        query_usuario = """
            INSERT INTO Usuarios (id_tipo_usuario, nombre, apellido_paterno, apellido_materno, correo, telefono, fecha_registro, usuario, password, status)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s)
        """
        cursor.execute(query_usuario, (1, nombre, apellido_paterno, apellido_materno, correo, telefono, usuario, password, status))

        # Obtener el ID del nuevo usuario
        id_usuario = cursor.lastrowid

        # Paso 2: Insertar en Administradores
        query_admin = """
            INSERT INTO Administradores (id_usuario, id_departamento, status)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query_admin, (id_usuario, id_departamento, status))

        con.commit()
        messagebox.showinfo("Éxito", "Administrador insertado correctamente.")
        mostrar_pantalla_principal(frame)
    except Exception as e:
        messagebox.showerror("Error", f"Error al insertar administrador: {e}")
    finally:
        con.close()


def actualizar_administrador(id_usuario, nombre, apellido_paterno, apellido_materno, correo, telefono, usuario, password, id_departamento, status, frame):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()

        # Paso 1: Actualizar tabla Usuarios
        query_usuarios = """
            UPDATE Usuarios 
            SET nombre = %s, 
                apellido_paterno = %s, 
                apellido_materno = %s, 
                correo = %s, 
                telefono = %s, 
                usuario = %s, 
                password = %s, 
                status = %s 
            WHERE id = %s
        """
        valores_usuarios = (nombre, apellido_paterno, apellido_materno, correo, telefono, usuario, password, status, id_usuario)
        cursor.execute(query_usuarios, valores_usuarios)

        # Paso 2: Actualizar tabla Administradores
        query_admins = """
            UPDATE Administradores 
            SET id_departamento = %s,
                status = %s
            WHERE id_usuario = %s
        """
        valores_admins = (id_departamento, status, id_usuario)
        cursor.execute(query_admins, valores_admins)

        con.commit()
        messagebox.showinfo("Éxito", "Administrador actualizado correctamente.")
        mostrar_pantalla_principal(frame)

    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar administrador: {e}")
    finally:
        con.close()

def eliminar_administrador(id_usuario, frame):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()

        # Paso 1: Eliminar de Administradores
        cursor.execute("DELETE FROM Administradores WHERE id_usuario = %s", (id_usuario,))

        # Paso 2: Eliminar de Usuarios
        cursor.execute("DELETE FROM Usuarios WHERE id = %s", (id_usuario,))

        con.commit()
        messagebox.showinfo("Éxito", "Administrador eliminado correctamente.")
        mostrar_pantalla_principal(frame)

    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar administrador: {e}")
    finally:
        con.close()

def guardar_administrador(nombre, apellido_paterno, apellido_materno, correo, telefono, usuario, password, departamento_id, estatus, frame):
    if not (nombre and apellido_paterno and apellido_materno and correo and telefono and usuario and password and departamento_id and estatus):
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()

        # Paso 1: Insertar en Usuarios
        query_usuarios = """
            INSERT INTO Usuarios (id_tipo_usuario, nombre, apellido_paterno, apellido_materno, correo, telefono, usuario, password, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores_usuarios = (1, nombre, apellido_paterno, apellido_materno, correo, telefono, usuario, password, estatus)
        cursor.execute(query_usuarios, valores_usuarios)

        # Obtener el ID del nuevo usuario
        id_usuario = cursor.lastrowid

        # Paso 2: Insertar en Administradores
        query_admin = "INSERT INTO Administradores (id_usuario, id_departamento, status) VALUES (%s, %s, %s)"
        cursor.execute(query_admin, (id_usuario, departamento_id, estatus))

        con.commit()
        messagebox.showinfo("Éxito", "Administrador guardado exitosamente.")
        mostrar_pantalla_principal(frame)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")
    finally:
        con.close()

def mostrar_pantalla_principal(frame):
    limpiar_frame(frame)

    tk.Label(frame, text="Módulo de Gestión de Administradores", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    # Búsqueda
    busqueda_frame = tk.Frame(frame, bg=FONDO_GENERAL)
    busqueda_frame.pack(pady=5)
    tk.Label(busqueda_frame, text="Buscar por ID o Nombre del Administrador:", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(side="left")
    entrada_busqueda = tk.Entry(busqueda_frame)
    entrada_busqueda.pack(side="left", padx=5)

    entrada_busqueda.bind("<KeyRelease>", lambda event: filtrar_administradores())

    # Tabla
    tabla_frame = tk.Frame(frame)
    tabla_frame.pack(expand=True, fill="both", padx=10, pady=10)

    cols = ["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Correo", "Teléfono", "Departamento", "Estatus"]
    tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8, style="Custom.Treeview")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    def mostrar_administradores():
        for i in tree.get_children():
            tree.delete(i)

        datos = obtener_datos_administradores()
        for row in datos:
            tree.insert("", "end", values=row)

    def filtrar_administradores():
        texto = entrada_busqueda.get().lower()
        datos = obtener_datos_administradores()
        filtrados = [fila for fila in datos if texto in str(fila[0]).lower() or texto in fila[1].lower()]
        for i in tree.get_children():
            tree.delete(i)
        for fila in filtrados:
            tree.insert("", "end", values=fila)

    mostrar_administradores()

    # Botones
    frame_btns = tk.Frame(frame, bg=FONDO_GENERAL)
    frame_btns.pack(pady=10)

    ttk.Button(frame_btns, text="Agregar ➕", style="Green.TButton",
               command=lambda: mostrar_pantalla_agregar(frame)).pack(side="left", padx=10)
    ttk.Button(frame_btns, text="Editar 📝", style="Blue.TButton",
               command=lambda: editar_registro(frame, tree)).pack(side="left", padx=10)
    ttk.Button(frame_btns, text="Eliminar ❌", style="Red.TButton",
               command=lambda: eliminar_registro(tree, frame)).pack(side="left", padx=10)

import tkinter as tk
from tkinter import ttk, messagebox

def mostrar_pantalla_agregar(frame):
    limpiar_frame(frame)

    frame.config(bg=FONDO_GENERAL)

    # Configurar columnas para centrar el contenido
    frame.columnconfigure(0, weight=1)  # espacio izquierdo flexible
    frame.columnconfigure(1, weight=1)  # espacio derecho flexible

    titulo = tk.Label(frame, text="Agregar Administrador", font=("Arial", 18, "bold"), bg=FONDO_GENERAL, fg="#333333")
    # El título ocupa ambas columnas, centrado
    titulo.grid(row=0, column=0, columnspan=2, pady=(15, 25), sticky="nsew")

    departamentos = obtener_datos_departamentos()
    departamentos_activos = [d for d in departamentos if d[2] == 1]

    campos = [
        ("Nombre", tk.StringVar()),
        ("Apellido Paterno", tk.StringVar()),
        ("Apellido Materno", tk.StringVar()),
        ("Correo", tk.StringVar()),
        ("Teléfono", tk.StringVar()),
        ("Usuario", tk.StringVar()),
        ("Contraseña", tk.StringVar()),
        ("Estatus (1=Activo, 0=Inactivo)", tk.StringVar())
    ]

    entradas = {}

    # Etiquetas a la derecha, entradas a la izquierda pero todo centrado en columnas balanceadas
    for i, (label_text, var) in enumerate(campos, start=1):
        etiqueta = ttk.Label(frame, text=label_text + ":", font=('Segoe UI', 11))
        etiqueta.grid(row=i, column=0, sticky="e", padx=(0, 10), pady=8)

        show = "*" if label_text == "Contraseña" else ""
        entrada = ttk.Entry(frame, textvariable=var, show=show, width=30)
        entrada.grid(row=i, column=1, sticky="w", padx=(10, 0), pady=8)

        entradas[label_text] = var

    etiqueta_depto = ttk.Label(frame, text="Departamento:", font=('Segoe UI', 11))
    etiqueta_depto.grid(row=len(campos)+1, column=0, sticky="e", padx=(0, 10), pady=8)

    combo_departamentos_var = tk.StringVar()
    combo_departamentos = ttk.Combobox(frame, textvariable=combo_departamentos_var, state="readonly", width=28)
    nombres_departamentos = [d[1] for d in departamentos_activos]
    combo_departamentos['values'] = nombres_departamentos
    combo_departamentos.grid(row=len(campos)+1, column=1, sticky="w", padx=(10, 0), pady=8)

    if nombres_departamentos:
        combo_departamentos.current(0)

    def guardar():
        try:
            telefono = int(entradas["Teléfono"].get())
            estatus = int(entradas["Estatus (1=Activo, 0=Inactivo)"].get())

            nombre_seleccionado = combo_departamentos_var.get()
            id_departamento = None
            for d in departamentos_activos:
                if d[1] == nombre_seleccionado:
                    id_departamento = d[0]
                    break

            if id_departamento is None:
                messagebox.showerror("Error", "Selecciona un departamento válido.")
                return

            insertar_administrador(
                entradas["Nombre"].get(),
                entradas["Apellido Paterno"].get(),
                entradas["Apellido Materno"].get(),
                entradas["Correo"].get(),
                telefono,
                entradas["Usuario"].get(),
                entradas["Contraseña"].get(),
                id_departamento,
                estatus,
                frame
            )
        except ValueError:
            messagebox.showerror("Error", "Teléfono y Estatus deben ser números válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    boton_guardar = ttk.Button(frame, text="Guardar", style="Green.TButton", command=guardar)
    boton_guardar.grid(row=len(campos)+2, column=0, columnspan=2, pady=(25, 10), ipadx=15, ipady=6)

    boton_volver = ttk.Button(frame, text="← Volver", command=lambda: mostrar_pantalla_principal(frame))
    boton_volver.grid(row=len(campos)+3, column=0, columnspan=2, pady=(5, 20), ipadx=15, ipady=6)


def eliminar_registro(tree, frame):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un registro para eliminar.")
        return
    item = tree.item(seleccion)
    datos = item['values']
    id_usuario = datos[0]
    confirmar = messagebox.askyesno("Confirmar", f"¿Quieres eliminar al administrador {datos[1]}?")
    if confirmar:
        eliminar_administrador(id_usuario, frame)


def editar_registro(frame, tree):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un registro para editar.")
        return
    item = tree.item(seleccion)
    datos = item['values']
    # Aquí abres una ventana o formulario con los datos para editar
    mostrar_pantalla_editar(frame, datos)

def mostrar_pantalla_editar(frame, datos):
    limpiar_frame(frame)

    tk.Label(frame, text="Editar Administrador", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    # Campos que sí tienes:
    campos_text = [
        "Nombre", "Apellido Paterno", "Apellido Materno",
        "Correo", "Teléfono", "Departamento", "Estatus (1=Activo, 0=Inactivo)"
    ]

    entradas = {}

    # Carga lista de departamentos (id, nombre)
    departamentos = obtener_datos_departamentos()
    nombres_departamentos = [d[1] for d in departamentos]

    for label_text in campos_text:
        tk.Label(frame, text=label_text + ":", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(pady=5)
        if label_text == "Departamento":
            var = tk.StringVar()
            combo = ttk.Combobox(frame, values=nombres_departamentos, textvariable=var, state="readonly")
            combo.pack(pady=5)
            # Seleccionar el departamento actual por nombre:
            departamento_actual = datos[6]  # índice 6 es el nombre departamento
            if departamento_actual in nombres_departamentos:
                var.set(departamento_actual)
            else:
                var.set(nombres_departamentos[0] if nombres_departamentos else "")
            entradas[label_text] = var
        else:
            var = tk.StringVar()
            entry = tk.Entry(frame, textvariable=var)
            entry.pack(pady=5)
            # Mapear índices de datos a campos_text:
            indice_map = {
                "Nombre": 1,
                "Apellido Paterno": 2,
                "Apellido Materno": 3,
                "Correo": 4,
                "Teléfono": 5,
                "Estatus (1=Activo, 0=Inactivo)": 7,
            }
            if label_text in indice_map:
                var.set(str(datos[indice_map[label_text]]))
            entradas[label_text] = var

    id_usuario = datos[0]

    def guardar():
        try:
            telefono = int(entradas["Teléfono"].get())
            estatus = int(entradas["Estatus (1=Activo, 0=Inactivo)"].get())

            # Obtener id del departamento seleccionado
            depto_nombre_seleccionado = entradas["Departamento"].get()
            id_depto = None
            for d in departamentos:
                if d[1] == depto_nombre_seleccionado:
                    id_depto = d[0]
                    break

            actualizar_administrador(
                id_usuario,
                entradas["Nombre"].get(),
                entradas["Apellido Paterno"].get(),
                entradas["Apellido Materno"].get(),
                entradas["Correo"].get(),
                telefono,
                # Si necesitas usuario y contraseña, debes obtenerlos de otro modo, aquí no los tienes
                "",  # usuario vacío, o el que tengas si lo guardas
                "",  # contraseña vacía
                id_depto,
                estatus,
                frame
            )
        except ValueError:
            messagebox.showerror("Error", "Teléfono y Estatus deben ser números válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    ttk.Button(
        frame,
        text="Guardar",
        style="Green.TButton",
        command=guardar
    ).pack(pady=10)

    tk.Button(
        frame,
        text="← Volver",
        bg="lightgray",
        command=lambda: mostrar_pantalla_principal(frame)
    ).pack(pady=10)
