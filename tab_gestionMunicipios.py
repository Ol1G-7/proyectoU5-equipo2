import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constantes import FONDO_GENERAL
import mysql.connector

def obtener_datos_municipios():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        query = """
            SELECT m.id, e.nombre AS estado, m.nombre, m.status, m.id_estado
            FROM Municipios m
            JOIN Estados e ON m.id_estado = e.id
        """
        cursor.execute(query)
        datos = cursor.fetchall()
        return datos if datos else [] 
    finally:
        con.close()

def obtener_estados():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        cursor.execute("SELECT id, nombre FROM Estados")
        datos = cursor.fetchall()
        return datos if datos else [] 
    finally:
        con.close()
        
def iniciar_modulo_municipios(frame_contenido):
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    mostrar_pantalla_principal(frame_contenido)

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def insertar_municipio(nombre, estatus, estado_combo, estados, frame):
    estado_seleccionado = estado_combo.get()

    estado_id = None
    for e in estados:
        if estado_seleccionado.startswith(e[1]):
            estado_id = e[0]
            break

    if not nombre or not estatus or not estado_id:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos correctamente.")
        return

    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        query = "INSERT INTO Municipios (nombre, status, id_estado) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, estatus, estado_id))
        con.commit()
        messagebox.showinfo("Éxito", "Municipio guardado exitosamente.")
        mostrar_pantalla_principal(frame)
    except Exception as e:
        messagebox.showerror("Error", f"Error al insertar municipio: {e}")
    finally:
        con.close()

def actualizar_municipio(id_municipio, estado_id, nombre, estatus, frame): 
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        query = "UPDATE Municipios SET id_estado = %s, nombre = %s, status = %s WHERE id = %s"
        cursor.execute(query, (estado_id, nombre, estatus, id_municipio))
        con.commit()
        mostrar_pantalla_principal(frame)
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar municipio: {e}")
    finally:
        con.close()
    
def guardar_edicion_municipio(id_municipio, nombre, estatus, estado_combo, estados, frame):
    estado_seleccionado = estado_combo.get()
    
    estado_id = None
    for e in estados:
        if estado_seleccionado.startswith(e[1]):
            estado_id = e[0]
            break

    if not nombre or not estatus or not estado_id:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos correctamente.")
        return

    actualizar_municipio(id_municipio, estado_id, nombre, estatus, frame)
    messagebox.showinfo("Éxito", "Municipio actualizado correctamente.")
    mostrar_pantalla_principal(frame)

def eliminar_municipio(id_municipio, frame):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        query = "DELETE FROM Municipios WHERE id = %s"
        cursor.execute(query, (id_municipio,))
        con.commit()
        messagebox.showinfo("Éxito", "Municipio eliminado correctamente.")
        mostrar_pantalla_principal(frame)
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar municipio: {e}")
    finally:
        con.close()

def mostrar_pantalla_principal(frame):
    limpiar_frame(frame)

    tk.Label(frame, text="Gestión de Municipios", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    busqueda_frame = tk.Frame(frame, bg=FONDO_GENERAL)
    busqueda_frame.pack(pady=5)
    tk.Label(busqueda_frame, text="Buscar por nombre del municipio o estado:", bg=FONDO_GENERAL).pack(side="left")
    entrada_busqueda = tk.Entry(busqueda_frame)
    entrada_busqueda.pack(side="left", padx=5)
    
    entrada_busqueda.bind("<KeyRelease>", lambda event: filtrar())

    tabla_frame = tk.Frame(frame)
    tabla_frame.pack(expand=True, fill="both", padx=10, pady=10)

    cols = ["ID", "Estado", "Municipio", "Estatus"]
    tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    def cargar_datos():
        for i in tree.get_children():
            tree.delete(i)
        for fila in obtener_datos_municipios():
            tree.insert("", "end", values=fila)

    def filtrar():
        texto = entrada_busqueda.get().lower()
        datos = obtener_datos_municipios()
        filtrados = [f for f in datos if texto in f[1].lower() or texto in f[2].lower()]
        for i in tree.get_children():
            tree.delete(i)
        for fila in filtrados:
            tree.insert("", "end", values=fila)

    cargar_datos()

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

    tk.Label(frame, text="Agregar Municipio", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    estados = obtener_estados()
    
    tk.Label(frame, text="Estado:", bg=FONDO_GENERAL).pack()
    estado_combo = ttk.Combobox(frame, values=[f"{e[1]} (ID: {e[0]})" for e in estados], state="readonly")
    estado_combo.pack()

    tk.Label(frame, text="Nombre del Municipio:", bg=FONDO_GENERAL).pack()
    entrada_nombre = tk.Entry(frame)
    entrada_nombre.pack()

    tk.Label(frame, text="Estatus:", bg=FONDO_GENERAL).pack()
    entrada_estatus = tk.Entry(frame)
    entrada_estatus.pack()
    
    ttk.Button(
        frame,
        text="Guardar",
        style="Green.TButton",
        command=lambda: insertar_municipio(
            entrada_nombre.get(),
            entrada_estatus.get(),
            estado_combo,
            estados,
            frame
        )
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
    confirmar = messagebox.askyesno("Confirmar", f"¿Quieres eliminar el registro {datos[2]}?")
    if confirmar:
        eliminar_municipio(datos[0], frame)

def editar_registro(frame, tree):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un registro para editar.")
        return
    item = tree.item(seleccion)
    datos = item['values']
    mostrar_pantalla_editar(frame, datos)

def mostrar_pantalla_editar(frame, datos):
    limpiar_frame(frame)

    tk.Label(frame, text="Editar Municipio", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    estados = obtener_estados()

    tk.Label(frame, text="Estado:", bg=FONDO_GENERAL).pack()
    estado_combo = ttk.Combobox(frame, values=[f"{e[1]} (ID: {e[0]})" for e in estados], state="readonly")
    estado_combo.pack()
    
    for e in estados:
        if e[1] == datos[1]:
            estado_combo.set(f"{e[1]} (ID: {e[0]})")
            break

    tk.Label(frame, text="Nombre del Municipio:", bg=FONDO_GENERAL).pack()
    entrada_nombre = tk.Entry(frame)
    entrada_nombre.pack()
    entrada_nombre.insert(0, datos[2])

    tk.Label(frame, text="Estatus:", bg=FONDO_GENERAL).pack()
    entrada_estatus = tk.Entry(frame)
    entrada_estatus.pack()
    entrada_estatus.insert(0, datos[3])

    id_municipio = datos[0]

    ttk.Button(
        frame,
        text="Guardar",
        style="Green.TButton",
        command=lambda: guardar_edicion_municipio(
            id_municipio,
            entrada_nombre.get(),
            entrada_estatus.get(),
            estado_combo,
            estados,
            frame
        )
    ).pack(pady=10)

    tk.Button(frame, text="← Volver", bg="lightgray", command=lambda: mostrar_pantalla_principal(frame)).pack(pady=10)
