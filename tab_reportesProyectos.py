import tkinter as tk
from tkinter import ttk
from constantes import FONDO_GENERAL
import mysql.connector

def buscar_voluntariado_por_nombre(nombre):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="TopicosProyectoDB"
    )
    cursor = con.cursor()
    query = "SELECT id, descripcion, fecha_inicio, fecha_fin FROM Voluntariados WHERE nombre = %s"
    cursor.execute(query, (nombre,))
    resultado = cursor.fetchone()
    con.close()
    return resultado

def actualizar_datos(event):
    nombre = combo_proyecto.get()
    resultado = buscar_voluntariado_por_nombre(nombre)
    if resultado:
        id_vol, descripcion, fecha_inicio_val, fecha_fin_val = resultado
        global id_seleccionado
        id_seleccionado = id_vol 

        desc_text.delete("1.0", "end")
        desc_text.insert("1.0", descripcion)

        fecha_inicio.delete(0, "end")
        fecha_inicio.insert(0, str(fecha_inicio_val))

        fecha_fin.delete(0, "end")
        fecha_fin.insert(0, str(fecha_fin_val))
        
        participantes = obtener_participantes_por_voluntariado(id_vol)
        mostrar_participantes_en_tabla(participantes)

def cargar_nombres_proyectos():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="TopicosProyectoDB"
    )
    cursor = con.cursor()
    cursor.execute("SELECT nombre FROM Voluntariados")
    resultados = cursor.fetchall()
    con.close()

    nombres = [fila[0] for fila in resultados] if resultados else []
    combo_proyecto['values'] = nombres
    if nombres:
        combo_proyecto.set(nombres[0])
    
    nombres.insert(0, "Seleccionar...")  
    combo_proyecto['values'] = nombres
    combo_proyecto.set("Seleccionar...")

def obtener_participantes_por_voluntariado(id_voluntariado):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="TopicosProyectoDB"
    )
    cursor = con.cursor()
    query = """
        SELECT 
            CONCAT(u.nombre, ' ', u.apellido_paterno, ' ', u.apellido_materno) AS nombre_completo,
            e.matricula,
            ve.horas_aportadas,
            ve.fecha_participacion
        FROM Voluntariados_Estudiantes ve
        JOIN Estudiantes e ON ve.id_estudiante = e.id_usuario
        JOIN Usuarios u ON e.id_usuario = u.id
        WHERE ve.id_voluntariado = %s;
    """
    cursor.execute(query, (id_voluntariado,))
    resultados = cursor.fetchall()
    con.close()
    return resultados

def mostrar_participantes_en_tabla(datos):
    for i in tree.get_children():
        tree.delete(i)
    for fila in datos:
        tree.insert("", "end", values=fila)

def crear_tab_reportesProyectos(notebook):
    
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Reportes de Proyectos")

    tk.Label(frame, text="Reportes de Proyectos", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

    contenedor_fila1 = tk.Frame(frame, bg=FONDO_GENERAL)
    contenedor_fila1.pack(pady=5)
    fila1 = tk.Frame(contenedor_fila1, bg=FONDO_GENERAL)
    fila1.pack()
    
    tk.Label(fila1, text="Proyecto:", bg=FONDO_GENERAL, font=("Segoe UI", 10)).pack(side="left", padx=5)
    global combo_proyecto
    combo_proyecto = ttk.Combobox(fila1, values=[], state="readonly", width=30)
    combo_proyecto.pack(side="left", padx=5)
    combo_proyecto.bind("<<ComboboxSelected>>", actualizar_datos)
    
    cargar_nombres_proyectos()

    tk.Label(fila1, text="Descripción:", bg=FONDO_GENERAL, font=("Segoe UI", 10)).pack(side="left", padx=15)
    global desc_text
    desc_text = tk.Text(fila1, height=2, width=50, wrap="word")
    desc_text.pack(side="left", padx=5)

    contenedor_fila2 = tk.Frame(frame, bg=FONDO_GENERAL)
    contenedor_fila2.pack(pady=5)
    fila2 = tk.Frame(contenedor_fila2, bg=FONDO_GENERAL)
    fila2.pack()

    tk.Label(fila2, text="Fecha Inicio:", bg=FONDO_GENERAL, font=("Segoe UI", 10)).pack(side="left", padx=5)
    global fecha_inicio
    fecha_inicio = tk.Entry(fila2, width=15)
    fecha_inicio.pack(side="left", padx=5)

    tk.Label(fila2, text="Fecha Fin:", bg=FONDO_GENERAL, font=("Segoe UI", 10)).pack(side="left", padx=15)
    global fecha_fin
    fecha_fin = tk.Entry(fila2, width=15)
    fecha_fin.pack(side="left", padx=5)

    tabla_frame = tk.Frame(frame)
    tabla_frame.pack(pady=15, fill="x")

    columnas = ("Nombre", "Matrícula", "Horas Aportadas", "Fecha Participación")
    global tree
    tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=6)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")

    scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    tree.pack(side="left", fill="x", expand=True)
