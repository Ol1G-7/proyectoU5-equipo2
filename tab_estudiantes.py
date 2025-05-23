import tkinter as tk
from tkinter import ttk,messagebox
from conexion_bd import obtener_estudiantes_desde_bd


def crear_tab_estudiantes(root, notebook, FONDO_GENERAL, style):
    notebook.pack_forget()

    frame_estudiantes = tk.Frame(root, bg=FONDO_GENERAL)
    frame_estudiantes.pack(fill="both", expand=True)


    navbar = tk.Frame(frame_estudiantes, bg="#3C88CF", height=60)
    navbar.pack(side="top", fill="x")
    tk.Label(navbar, text="🧩", font=("Arial", 20), bg="#3C88CF", fg="white").pack(side="left", padx=20)
    tk.Label(navbar, text="Gestión Estudiantes", font=("Arial", 12, "bold"),
             bg="#3C88CF", fg="white").pack(side="left")


    tk.Label(frame_estudiantes, text="Modulo De Gestión de Estudiantes",
             font=("Arial", 14, "bold"), bg=FONDO_GENERAL).pack(pady=10)


    busqueda_frame = tk.Frame(frame_estudiantes, bg=FONDO_GENERAL)
    busqueda_frame.pack(pady=5)
    tk.Label(busqueda_frame, text="Buscar por Nombre o Matrícula:", bg=FONDO_GENERAL,
             font=('Segoe UI', 10)).pack(side="left")
    entrada_busqueda = tk.Entry(busqueda_frame)
    entrada_busqueda.pack(side="left", padx=5)

    def filtrar_tabla():
        texto = entrada_busqueda.get().lower()
        filtrados = [fila for fila in estudiantes if texto in fila[0].lower() or texto in fila[1]]
        mostrar_datos(filtrados)

    tk.Button(busqueda_frame, text="Buscar", command=filtrar_tabla).pack(side="left", padx=5)

  
    columnas = ["Nombre Completo", "Matrícula", "Correo Institucional", "Carrera",
                "Voluntariado", "Fecha participación", "Horas", "Estado"]

    frame_tabla = tk.Frame(frame_estudiantes)
    frame_tabla.pack(fill="both", expand=True, padx=20)

    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8, style="Custom.Treeview")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=160)

    scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)


    estudiantes = obtener_estudiantes_desde_bd()


    def mostrar_datos(datos):
        tree.delete(*tree.get_children())
        for est in datos:
            tree.insert("", "end", values=est)

    mostrar_datos(estudiantes)  

    
    frame_botones = tk.Frame(frame_estudiantes, bg=FONDO_GENERAL)
    frame_botones.pack(pady=20)

    ttk.Button(
        frame_botones,
        text="Agregar Estudiante +",
        style="Green.TButton",
        command=lambda: abrir_formulario_registro(root, frame_estudiantes, notebook, FONDO_GENERAL, style)
    ).pack(side="left", padx=10)



    ttk.Button(
        frame_botones,
        text="Editar Registro",
        style="Blue.TButton",
        command=lambda: abrir_formulario_editar(root, frame_estudiantes, notebook, FONDO_GENERAL, style)
    ).pack(side="left", padx=10)

    ttk.Button(
        frame_botones,
        text="Ver Detalle",
        style="Yellow.TButton",
        command=lambda: abrir_detalle_estudiante(root, frame_estudiantes, notebook, FONDO_GENERAL, style)
    ).pack(side="left", padx=10)


    ttk.Button(
        frame_botones,
        text="Eliminar Estudiante ❌",
        style="Red.TButton",
        command=lambda: eliminar_estudiante(root, frame_estudiantes, notebook, FONDO_GENERAL, style, tree)
    ).pack(side="left", padx=10)



    def regresar():
        frame_estudiantes.destroy()
        notebook.pack(expand=True, fill="both")

    tk.Button(frame_estudiantes, text="← Regresar", bg="lightgray", command=regresar).pack(pady=10)

    def abrir_formulario_registro(root, frame_actual, notebook, FONDO_GENERAL, style):
        frame_actual.destroy()  
        from formulario_registro_estudiante import crear_formulario_estudiante
        crear_formulario_estudiante(root, notebook, FONDO_GENERAL, style)

    def abrir_formulario_editar(root, frame_actual, notebook, FONDO_GENERAL, style):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Debes seleccionar un estudiante.")
            return

        datos_fila = tree.item(seleccionado)['values']
        matricula = datos_fila[1]

        frame_actual.destroy()
        from formulario_editar_estudiante import crear_formulario_editar
        crear_formulario_editar(root, notebook, FONDO_GENERAL, style, matricula)


    def abrir_detalle_estudiante(root, frame_actual, notebook, FONDO_GENERAL, style):
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Debes seleccionar un estudiante.")
            return

        datos_fila = tree.item(seleccionado)['values']
        matricula = datos_fila[1] 

        frame_actual.destroy()
        from detalle_estudiante import crear_detalle_estudiante
        crear_detalle_estudiante(root, notebook, FONDO_GENERAL, style, matricula)


    return frame_estudiantes


from conexion_bd import conectar
from tkinter import messagebox

def eliminar_estudiante(root, frame_actual, notebook, FONDO_GENERAL, style, tree):
    seleccionado = tree.focus()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Debes seleccionar un estudiante.")
        return

    datos_fila = tree.item(seleccionado)["values"]
    matricula = datos_fila[1] 

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Seguro que deseas eliminar al estudiante con matrícula: {matricula}?"
    )
    if not confirmar:
        return

    try:
        con = conectar()
        cur = con.cursor()
        
        cur.execute("SELECT id_usuario FROM Estudiantes WHERE matricula = %s", (matricula,))
        estudiante = cur.fetchone()

        if not estudiante:
            messagebox.showerror("Error", "No se encontró el estudiante en la base de datos.")
            con.close()
            return

        id_usuario = estudiante[0]

      
        cur.execute("DELETE FROM Voluntariados_Estudiantes WHERE id_estudiante = %s", (id_usuario,))

      
        cur.execute("DELETE FROM Estudiantes WHERE id_usuario = %s", (id_usuario,))

      
        cur.execute("DELETE FROM Usuarios WHERE id = %s", (id_usuario,))

        con.commit()
        con.close()

        messagebox.showinfo("Éxito", f"Estudiante con matrícula {matricula} eliminado correctamente.")

     
        frame_actual.destroy()
        from tab_estudiantes import crear_tab_estudiantes
        crear_tab_estudiantes(root, notebook, FONDO_GENERAL, style)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el estudiante:\n{e}")
        if con:
            con.rollback()
            con.close()
