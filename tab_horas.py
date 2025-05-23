import tkinter as tk
from tkinter import ttk, messagebox
from constantes import FONDO_GENERAL
from conexion_bd import conectar
from tab_estudiantes import crear_tab_estudiantes

def obtener_datos_horas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            CONCAT(u.nombre, ' ', u.apellido_paterno, ' ', u.apellido_materno) AS nombre,
            e.matricula,
            u.correo,
            c.nombre AS carrera,
            v.nombre AS voluntariado,
            ve.fecha_participacion,
            ve.horas_aportadas,
            ve.estado_validacion,
            ve.observaciones
        FROM Voluntariados_Estudiantes ve
        JOIN Estudiantes e ON ve.id_estudiante = e.id_usuario
        JOIN Usuarios u ON e.id_usuario = u.id
        JOIN Carreras c ON e.id_carrera = c.id
        JOIN Voluntariados v ON ve.id_voluntariado = v.id;
    """)
    
    resultados = cursor.fetchall()
    conexion.close()
    return resultados if resultados else []


def crear_tab_horas(root, notebook, FONDO_GENERAL, style):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Aprobación de Horas")

    tk.Label(frame, text="Módulo de Aprobación de Horas", font=("Arial", 16, "bold"), bg=FONDO_GENERAL).pack(pady=10)

   
    busqueda_frame = tk.Frame(frame, bg=FONDO_GENERAL)
    busqueda_frame.pack(pady=5)
    tk.Label(busqueda_frame, text="Buscar por Nombre o Matrícula:", bg=FONDO_GENERAL, font=('Segoe UI', 10)).pack(side="left")
    entrada_busqueda = tk.Entry(busqueda_frame)
    entrada_busqueda.pack(side="left", padx=5)
    tk.Button(busqueda_frame, text="Buscar", command=lambda: filtrar_tabla()).pack(side="left", padx=5)

    tabla_frame = tk.Frame(frame)
    tabla_frame.pack(expand=True, fill="both", padx=10, pady=10)

    cols = ["Nombre", "Matrícula", "Correo", "Carrera", "Voluntariado", "Fecha", "Horas", "Estado", "Observaciones"]
    tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8, style="Custom.Treeview")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center", minwidth=130)

    scrollbar_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    datos_completos = []

    def mostrar_datos(datos):
        nonlocal datos_completos
        datos_completos = datos
        for i in tree.get_children():
            tree.delete(i)
        for row in datos:
            visible_row = list(row)
            visible_row[8] = "Ver" 
            tree.insert("", "end", values=visible_row)

    def filtrar_tabla():
        texto = entrada_busqueda.get().lower()
        datos_actualizados = obtener_datos_horas()
        filtrados = [fila for fila in datos_actualizados if texto in fila[0].lower() or texto in fila[1]]
        mostrar_datos(filtrados)

    def actualizar_estado(nuevo_estado):
        seleccion = tree.selection()
        if seleccion:
            item = seleccion[0]
            valores = tree.item(item, "values")
            matricula = valores[1]

            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("""
                    UPDATE Voluntariados_Estudiantes ve
                    JOIN Estudiantes e ON ve.id_estudiante = e.id_usuario
                    SET ve.estado_validacion = %s
                    WHERE e.matricula = %s
                """, (nuevo_estado, matricula))
                conexion.commit()
                conexion.close()

                messagebox.showinfo("Éxito", f"Estado actualizado a '{nuevo_estado}'.")
                mostrar_datos(obtener_datos_horas())
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")
        else:
            messagebox.showwarning("Sin selección", "Selecciona un registro para actualizar su estado.")

    
    def ver_info_estudiante():
        crear_tab_estudiantes(root, notebook, FONDO_GENERAL, style)

    def on_doble_click(event):
        item = tree.identify_row(event.y)
        col = tree.identify_column(event.x)

        if item and col == '#9':  
            valores = tree.item(item, "values")
            original = next((r for r in datos_completos if r[1] == valores[1]), None)
            observaciones = original[8] if original else "Sin observaciones."
            messagebox.showinfo("Observaciones", observaciones)

    tree.bind("<Double-1>", on_doble_click)


    frame_btns = tk.Frame(frame, bg=FONDO_GENERAL)
    frame_btns.pack(pady=10)

    ttk.Button(frame_btns, text="Aprobar ✅", style="Green.TButton",
               command=lambda: actualizar_estado("Aprobado")).pack(side="left", padx=10)

    ttk.Button(frame_btns, text="Rechazar ❌", style="Red.TButton",
               command=lambda: actualizar_estado("Rechazado")).pack(side="left", padx=10)

    ttk.Button(frame_btns, text="Ver Información del Estudiante 📄", style="Blue.TButton",
               command=ver_info_estudiante).pack(side="left", padx=10)
    
    mostrar_datos(obtener_datos_horas())

