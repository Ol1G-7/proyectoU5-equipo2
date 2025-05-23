import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constantes import FONDO_GENERAL
import mysql.connector

def obtener_datos_colaboradores():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        cursor.execute("SELECT id, nombre, apellido_paterno, apellido_materno, organizacion, telefono, correo, status FROM Colaboradores")
        datos = cursor.fetchall()
        return datos if datos else []
    finally:
        con.close()

def iniciar_modulo_colaboradores(frame_contenido):
    # Limpia el contenido anterior si es necesario
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    # Y luego llama a la pantalla principal en ese frame
    mostrar_pantalla_principal(frame_contenido)

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def insertar_colaborador(nombre, apellido_paterno, apellido_materno, organizacion, telefono, correo, estatus):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        query = "INSERT INTO Colaboradores (nombre, apellido_paterno, apellido_materno, organizacion, telefono, correo, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nombre, apellido_paterno, apellido_materno, organizacion, telefono, correo, estatus))
        con.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Error al insertar: {e}")
    finally:
        con.close()

def actualizar_colaborador(id_colaborador, nombre, apellido_paterno, apellido_materno, organizacion, telefono, correo, estatus, frame):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        query = """
            UPDATE Colaboradores 
            SET nombre = %s, 
                apellido_paterno = %s, 
                apellido_materno = %s, 
                organizacion = %s, 
                telefono = %s, 
                correo = %s, 
                status = %s 
            WHERE id = %s
        """
        valores = (nombre, apellido_paterno, apellido_materno, organizacion, telefono, correo, estatus, id_colaborador)
        cursor.execute(query, valores)
        con.commit()
        messagebox.showinfo("Éxito", "Colaborador actualizado correctamente.")
        mostrar_pantalla_principal(frame)
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar: {e}")
    finally:
        con.close()

def eliminar_colaborador(id_colaborador, frame):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        query = "DELETE FROM Colaboradores WHERE id = %s"
        cursor.execute(query, (id_colaborador,))
        con.commit()
        messagebox.showinfo("Éxito", "Colaborador eliminado correctamente.")
        mostrar_pantalla_principal(frame)
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar: {e}")
    finally:
        con.close()

def guardar_colaborador(nombre, apellido_paterno, apellido_materno, organizacion, telefono, correo, estatus, frame):
    if not (nombre and apellido_paterno and apellido_materno and organizacion and telefono and correo and estatus):
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    try:
        insertar_colaborador(nombre, apellido_paterno, apellido_materno, organizacion, telefono, correo, estatus)
        messagebox.showinfo("Éxito", "Colaborador guardado exitosamente.")
        mostrar_pantalla_principal(frame)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")


def mostrar_pantalla_principal(frame):
    
    limpiar_frame(frame)

    tk.Label(frame, text="Módulo de Gestión de Colaboradores", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    # Búsqueda
    busqueda_frame = tk.Frame(frame, bg=FONDO_GENERAL)
    busqueda_frame.pack(pady=5)
    tk.Label(busqueda_frame, text="Buscar por ID o Nombre del Colaborador:", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(side="left")
    entrada_busqueda = tk.Entry(busqueda_frame)
    entrada_busqueda.pack(side="left", padx=5)

    entrada_busqueda.bind("<KeyRelease>", lambda event: filtrar_proyectos())
    
    # Tabla
    tabla_frame = tk.Frame(frame)
    tabla_frame.pack(expand=True, fill="both", padx=10, pady=10)

    cols = ["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Organización", "Teléfono", "Correo", "Estatus"]
    tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8, style="Custom.Treeview")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    def mostrar_proyectos():
        for i in tree.get_children():
            tree.delete(i)

        datos = obtener_datos_colaboradores()
        for row in datos:
            tree.insert("", "end", values=row)

    def filtrar_proyectos():
        texto = entrada_busqueda.get().lower()
        datos = obtener_datos_colaboradores()
        filtrados = [fila for fila in datos if texto in str(fila[0]) or texto in fila[1].lower()]
        for i in tree.get_children():
            tree.delete(i)
        for fila in filtrados:
            tree.insert("", "end", values=fila)

    mostrar_proyectos()

    # Botones
    frame_btns = tk.Frame(frame, bg=FONDO_GENERAL)
    frame_btns.pack(pady=10)

    ttk.Button(frame_btns, text="Agregar ➕", style="Green.TButton",
               command=lambda: mostrar_pantalla_agregar(frame)).pack(side="left", padx=10)
    ttk.Button(frame_btns, text="Editar 📝", style="Blue.TButton",
               command=lambda: editar_registro(frame, tree)).pack(side="left", padx=10)
    ttk.Button(frame_btns, text="Eliminar ❌", style="Red.TButton",
               command=lambda: eliminar_registro(tree, frame)).pack(side="left", padx=10)

def mostrar_pantalla_agregar(frame):
    limpiar_frame(frame)

    tk.Label(frame, text="Agregar Colaborador", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    campos = [
        ("Nombre", tk.StringVar()),
        ("Apellido Paterno", tk.StringVar()),
        ("Apellido Materno", tk.StringVar()),
        ("Organización", tk.StringVar()),
        ("Teléfono", tk.StringVar()),
        ("Correo", tk.StringVar()),
        ("Estatus (1=Activo, 0=Inactivo)", tk.StringVar())
    ]

    entradas = {}

    for label_text, var in campos:
        tk.Label(frame, text=label_text + ":", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(pady=5)
        entry = tk.Entry(frame, textvariable=var)
        entry.pack(pady=5)
        entradas[label_text] = var

    def guardar():
        try:
            guardar_colaborador(
                entradas["Nombre"].get(),
                entradas["Apellido Paterno"].get(),
                entradas["Apellido Materno"].get(),
                entradas["Organización"].get(),
                int(entradas["Teléfono"].get()),
                entradas["Correo"].get(),
                int(entradas["Estatus (1=Activo, 0=Inactivo)"].get()),
                frame
            )
        except ValueError:
            messagebox.showerror("Error", "Teléfono y Estatus deben ser números válidos.")

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


def eliminar_registro(tree, frame):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un registro para eliminar.")
        return
    item = tree.item(seleccion)
    datos = item['values']
    # Confirmar eliminación
    confirmar = messagebox.askyesno("Confirmar", f"¿Quieres eliminar el registro {datos[1]}?")
    if confirmar:
        eliminar_colaborador(datos[0], frame)

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

    tk.Label(frame, text="Editar Colaborador", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    etiquetas = [
        "Nombre", "Apellido Paterno", "Apellido Materno",
        "Organización", "Teléfono", "Correo", "Estatus"
    ]

    variables = []
    for i, etiqueta in enumerate(etiquetas):
        tk.Label(frame, text=f"{etiqueta}:", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(pady=5)
        var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=var)
        entry.pack(pady=5)
        var.set(str(datos[i+1]))  # datos[0] = id, el resto son los valores
        variables.append(var)

    id_colaborador = datos[0]

    def guardar():
        try:
            actualizar_colaborador(
                id_colaborador,
                variables[0].get(),  # nombre
                variables[1].get(),  # apellido_paterno
                variables[2].get(),  # apellido_materno
                variables[3].get(),  # organizacion
                int(variables[4].get()),  # telefono
                variables[5].get(),  # correo
                int(variables[6].get()),  # estatus
                frame
            )
        except ValueError:
            messagebox.showerror("Error", "Teléfono y Estatus deben ser números válidos.")

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
