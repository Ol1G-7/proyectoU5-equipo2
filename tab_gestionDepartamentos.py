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

def iniciar_modulo_departamentos(frame_contenido):
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    mostrar_pantalla_principal(frame_contenido)

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def insertar_departamentos(nombre, estatus):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        query = "INSERT INTO Departamentos (nombre, status) VALUES (%s, %s)"
        cursor.execute(query, (nombre, estatus))
        con.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Error al insertar: {e}")
    finally:
        con.close()

def actualizar_departamento(id_departamento, nombre, estatus, frame):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        query = "UPDATE Departamentos SET nombre = %s, status = %s WHERE id = %s"
        cursor.execute(query, (nombre, estatus, id_departamento))
        con.commit()
        messagebox.showinfo("Éxito", "Departamento actualizado correctamente.")
        mostrar_pantalla_principal(frame)
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar: {e}")
    finally:
        con.close()


def eliminar_departamento(id_departamento, frame):
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = con.cursor()
        query = "DELETE FROM Departamentos WHERE id = %s"
        cursor.execute(query, (id_departamento,))
        con.commit()
        messagebox.showinfo("Éxito", "Departamento eliminado correctamente.")
        mostrar_pantalla_principal(frame)
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar: {e}")
    finally:
        con.close()

def guardar_departamento(nombre, estatus, frame):
    if not nombre or not estatus:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    insertar_departamentos(nombre, estatus)
    messagebox.showinfo("Éxito", "Departamento guardado exitosamente.")
    mostrar_pantalla_principal(frame)

def mostrar_pantalla_principal(frame):
    limpiar_frame(frame)

    tk.Label(frame, text="Módulo de Gestión de Departamentos", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    busqueda_frame = tk.Frame(frame, bg=FONDO_GENERAL)
    busqueda_frame.pack(pady=5)
    tk.Label(busqueda_frame, text="Buscar por ID o Nombre del Departamento:", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(side="left")
    entrada_busqueda = tk.Entry(busqueda_frame)
    entrada_busqueda.pack(side="left", padx=5)

    entrada_busqueda.bind("<KeyRelease>", lambda event: filtrar_departamentos())

    tabla_frame = tk.Frame(frame)
    tabla_frame.pack(expand=True, fill="both", padx=10, pady=10)

    cols = ["ID", "Nombre", "Estatus"]
    tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8, style="Custom.Treeview")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    def mostrar_departamentos():
        for i in tree.get_children():
            tree.delete(i)

        datos = obtener_datos_departamentos()
        for row in datos:
            tree.insert("", "end", values=row)

    def filtrar_departamentos():
        texto = entrada_busqueda.get().lower()
        datos = obtener_datos_departamentos()
        filtrados = [fila for fila in datos if texto in str(fila[0]) or texto in fila[1].lower()]
        for i in tree.get_children():
            tree.delete(i)
        for fila in filtrados:
            tree.insert("", "end", values=fila)

    mostrar_departamentos()

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

    tk.Label(frame, text="Agregar Departamento", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    tk.Label(frame, text="Nombre del Departamento:", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(pady=5)
    entrada_nombre = tk.Entry(frame)
    entrada_nombre.pack(pady=5)

    tk.Label(frame, text="Estatus:", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(pady=5)
    entrada_estatus = tk.Entry(frame)
    entrada_estatus.pack(pady=5)
    
    ttk.Button(
        frame,
        text="Guardar",
        style="Green.TButton",
        command=lambda: guardar_departamento(entrada_nombre.get(), entrada_estatus.get(), frame)
    ).pack(pady=10)
    tk.Button(frame, text="← Volver", bg="lightgray", command=lambda: mostrar_pantalla_principal(frame)).pack(pady=10)

def eliminar_registro(tree, frame):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un registro para eliminar.")
        return
    item = tree.item(seleccion)
    datos = item['values']
    confirmar = messagebox.askyesno("Confirmar", f"¿Quieres eliminar el registro {datos[1]}?")
    if confirmar:
        eliminar_departamento(datos[0], frame)

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

    tk.Label(frame, text="Editar Departamento", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    tk.Label(frame, text="Nombre del Departamento:", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(pady=5)
    entrada_nombre = tk.Entry(frame)
    entrada_nombre.pack(pady=5)
    entrada_nombre.insert(0, datos[1])

    tk.Label(frame, text="Estatus:", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(pady=5)
    entrada_estatus = tk.Entry(frame)
    entrada_estatus.pack(pady=5)
    entrada_estatus.insert(0, datos[2])
    
    id_estado = datos[0]
    
    ttk.Button(
        frame,
        text="Guardar",
        style="Green.TButton",
        command=lambda: actualizar_departamento(id_estado, entrada_nombre.get(), entrada_estatus.get(), frame)
    ).pack(pady=10)
    tk.Button(frame, text="← Volver", bg="lightgray", command=lambda: mostrar_pantalla_principal(frame)).pack(pady=10)
