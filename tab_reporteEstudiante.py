from conexion_bd import conectar
import tkinter as tk
from tkinter import ttk, messagebox
from constantes import FONDO_GENERAL

def crear_tab_horasE(notebook, id_usuario):
    id_usu = id_usuario
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Reporte de Horas")

    tk.Label(frame, text="Módulo de Reporte de Horas", font=("Arial", 16, "bold"), bg='white').pack(pady=10)

    # Entrada para buscar por ID de usuario
    buscar_frame = tk.Frame(frame, bg='white')
    buscar_frame.pack(pady=5)

    def obtener_reporte_voluntariado(id_usuario):
        conexion = conectar()
        cursor = conexion.cursor()

        # Primer SELECT: historial
        cursor.execute("""
            SELECT 
                v.nombre AS nombre_proyecto,
                ve.fecha_participacion,
                ve.horas_aportadas,
                ve.estado_validacion,
                CONCAT(u_resp.nombre, ' ', u_resp.apellido_paterno, ' ', u_resp.apellido_materno) AS responsable,
                ve.observaciones
            FROM Voluntariados_Estudiantes ve
            JOIN Estudiantes e ON ve.id_estudiante = e.id_usuario
            JOIN Usuarios u ON e.id_usuario = u.id
            JOIN Carreras c ON e.id_carrera = c.id
            JOIN Voluntariados v ON ve.id_voluntariado = v.id
            JOIN Usuarios u_resp ON v.id_responsable = u_resp.id
            WHERE e.id_usuario = %s
            ORDER BY ve.fecha_participacion;
        """, (id_usuario,))
        historial = cursor.fetchall()

        # Segundo SELECT: total de horas
        cursor.execute("""
            SELECT SUM(ve.horas_aportadas)
            FROM Voluntariados_Estudiantes ve
            JOIN Estudiantes e ON ve.id_estudiante = e.id_usuario
            WHERE e.id_usuario = %s;
        """, (id_usuario,))
        result = cursor.fetchone()
        total_horas = result[0] if result and result[0] is not None else 0

        conexion.close()
        return historial, total_horas

    # Tabla
    tabla_frame = tk.Frame(frame)
    tabla_frame.pack(expand=True, fill="both", padx=10, pady=10)

    cols = ["Voluntariado", "Fecha", "Horas", "Estado", "Responsable"]
    tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8, style="Custom.Treeview")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center", minwidth=130)

    scrollbar_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Etiqueta de total de horas
    total_label = tk.Label(frame, text="", bg='white', font=("Arial", 12, "bold"))
    total_label.pack(pady=5)

    def mostrar_reporte():
        id_usuario = str(id_usu)
        if not id_usuario.isdigit():
            messagebox.showwarning("Entrada inválida", "Por favor ingresa un ID válido.")
            return

        historial, total_horas = obtener_reporte_voluntariado(int(id_usuario))
        for i in tree.get_children():
            tree.delete(i)

        if historial is None:
            historial = []

        for fila in historial:
            tree.insert("", "end", values=fila[:9])  # observaciones no se muestran directamente

        total_label.config(text=f"Total de horas acumuladas: {total_horas} horas")

    mostrar_reporte()
