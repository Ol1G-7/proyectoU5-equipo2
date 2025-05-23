import tkinter as tk
from tkinter import ttk, messagebox
from constantes import FONDO_GENERAL
from conexion import obtener_conexion


def obtener_datos_proyectos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            v.id,
            v.nombre,
            v.actividades,
            v.descripcion,
            v.objetivo,
            tv.nombre AS tipo,
            v.fecha_inicio,
            v.fecha_fin,
            CONCAT(r.nombre, ' ', r.apellido_paterno, ' ', r.apellido_materno) AS responsable,
            CONCAT(dv.calle, ' ', dv.numero, ', ', dv.colonia) AS direccion,
            v.vacantes,
            CASE WHEN v.status = 1 THEN 'Activo' ELSE 'Inactivo' END
        FROM Voluntariados v
        JOIN Tipos_Voluntariados tv ON v.id_tipo = tv.id
        JOIN Responsables r ON v.id_responsable = r.id
        JOIN Direcciones_Voluntariados dv ON v.id = dv.id_voluntariado
    """)

    resultados = cursor.fetchall()
    conexion.close()

    datos_visibles = []
    textos_extras = {}  

    for fila in resultados:
        id_vol, nombre, actividades, descripcion, objetivo, tipo, inicio, fin, responsable, direccion, vacantes, estatus = fila
        datos_visibles.append((id_vol, nombre, "Ver", tipo, inicio, fin, responsable, direccion, vacantes, estatus))
        textos_extras[id_vol] = {
            "objetivo": objetivo,
            "actividades": actividades,
            "descripcion": descripcion
        }

    return datos_visibles, textos_extras


def crear_tab_proyectos(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Gestión de Proyectos")

    tk.Label(frame, text="Módulo de Gestión de Proyectos", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)


    busqueda_frame = tk.Frame(frame, bg=FONDO_GENERAL)
    busqueda_frame.pack(pady=5)
    tk.Label(busqueda_frame, text="Buscar por ID o Nombre del Proyecto:", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(side="left")
    entrada_busqueda = tk.Entry(busqueda_frame)
    entrada_busqueda.pack(side="left", padx=5)


    tabla_frame = tk.Frame(frame)
    tabla_frame.pack(expand=True, fill="both", padx=10, pady=10)

    cols = ["ID", "Nombre Voluntariado", "Objetivo", "Tipo", "Inicio", "Fin", "Responsable", "Dirección", "Vacantes", "Estatus"]
    tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8, style="Custom.Treeview")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

  
    frame_detalles = tk.Frame(frame, bg=FONDO_GENERAL)
    frame_detalles.pack(pady=15, fill="x", padx=20)

    tk.Label(frame_detalles, text="ACTIVIDADES", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10)
    tk.Label(frame_detalles, text="DESCRIPCIÓN", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)

    txt_actividades = tk.Text(frame_detalles, height=5, width=50)
    txt_actividades.grid(row=1, column=0, padx=10, pady=5)

    txt_descripcion = tk.Text(frame_detalles, height=5, width=50)
    txt_descripcion.grid(row=1, column=1, padx=10, pady=5)

    datos_proyectos, textos_extra = obtener_datos_proyectos()

    def mostrar_proyectos(datos):
        for i in tree.get_children():
            tree.delete(i)
        for row in datos:
            tree.insert("", "end", values=row)

    def filtrar_proyectos():
        texto = entrada_busqueda.get().lower()
        datos_actualizados, nuevos_extras = obtener_datos_proyectos()
        filtrados = [fila for fila in datos_actualizados if texto in str(fila[0]) or texto in fila[1].lower()]
        mostrar_proyectos(filtrados)
        textos_extra.clear()
        textos_extra.update(nuevos_extras)

    mostrar_proyectos(datos_proyectos)

    tk.Button(busqueda_frame, text="Buscar", command=filtrar_proyectos).pack(side="left", padx=5)


    def manejar_click(evento):
        item = tree.identify_row(evento.y)
        columna = tree.identify_column(evento.x)
        if item:
            valores = tree.item(item, "values")
            id_vol = int(valores[0])
            col_index = int(columna[1:]) - 1  # de "#3" a 2

            if col_index == 2:
                objetivo = textos_extra[id_vol]["objetivo"]
                messagebox.showinfo("Objetivo del Voluntariado", objetivo)

    def al_seleccionar_fila(evento):
        item = tree.selection()
        if item:
            valores = tree.item(item, "values")
            id_vol = int(valores[0])

            txt_actividades.delete("1.0", tk.END)
            txt_descripcion.delete("1.0", tk.END)

            txt_actividades.insert(tk.END, textos_extra[id_vol]["actividades"])
            txt_descripcion.insert(tk.END, textos_extra[id_vol]["descripcion"])

    tree.bind("<Double-1>", manejar_click)
    tree.bind("<<TreeviewSelect>>", al_seleccionar_fila)

    frame_btns = tk.Frame(frame, bg=FONDO_GENERAL)
    frame_btns.pack(pady=10)

    ttk.Button(frame_btns, text="Agregar ➕", style="Green.TButton").pack(side="left", padx=10)
    ttk.Button(frame_btns, text="Editar 📝", style="Blue.TButton").pack(side="left", padx=10)
    ttk.Button(frame_btns, text="Eliminar ❌", style="Red.TButton").pack(side="left", padx=10)

    tk.Button(frame, text="← Home", bg="lightgray").pack(pady=10)

