import tkinter as tk
from tkinter import ttk, messagebox
from conexion_bd import conectar
from conexion_bd import obtener_datos_estudiante

def crear_formulario_editar(root, notebook, FONDO_GENERAL, style, matricula):
    notebook.pack_forget()

    frame_edit = tk.Frame(root, bg=FONDO_GENERAL)
    frame_edit.pack(fill="both", expand=True)


    navbar = tk.Frame(frame_edit, bg="#3C88CF", height=60)
    navbar.pack(side="top", fill="x")
    tk.Label(navbar, text="🧩", font=("Arial", 24), bg="#3C88CF", fg="white").pack(side="left", padx=20)
    tk.Label(navbar, text="Editar Registro Estudiante", font=("Arial", 14, "bold"),
             bg="#3C88CF", fg="white").pack(side="left")


    tk.Label(frame_edit, text="Modulo De Gestión de Estudiantes", font=("Arial", 14, "bold"),
             bg=FONDO_GENERAL).pack(pady=10)


    form_frame = tk.Frame(frame_edit, bg="white", padx=30, pady=30)
    form_frame.pack(padx=20, pady=10)

    datos = obtener_datos_estudiante(matricula)
    if datos is None:
        messagebox.showerror("Error", f"No se encontraron datos para la matrícula: {matricula}")
        regresar(frame_edit, root, notebook, FONDO_GENERAL, style)
        return


    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nombre FROM Carreras WHERE status=1")
    carreras = cur.fetchall()
    cur.execute("SELECT id, nombre FROM Voluntariados WHERE status=1")
    voluntariados = cur.fetchall()
    con.close()

    combobox_ids = {
        "Carrera": {c[1]: c[0] for c in carreras} if carreras else {},
        "Voluntariado": {v[1]: v[0] for v in voluntariados} if voluntariados else {}
    }

    campos = [
        ("Nombre:", datos["nombre"]),
        ("Matrícula:", datos["matricula"]),
        ("Apellido Paterno:", datos["apellido_paterno"]),
        ("Carrera:", datos["carrera"]),
        ("Apellido Materno:", datos["apellido_materno"]),
        ("Voluntariado:", datos["voluntariado"] or ""),
        ("Correo:", datos["correo"]),
        ("Teléfono:", str(datos["telefono"])),
        ("Fecha de registro:", str(datos["fecha_registro"])),
        ("Usuario:", datos["usuario"]),
        ("Contraseña:", datos["password"])
    ]

    voluntariado_extra = [
        ("Fecha de participación:", datos["fecha_participacion"].strftime("%Y-%m-%d") if datos["fecha_participacion"] else ""),
        ("Horas Aportadas:", str(datos["horas_aportadas"]) if datos["horas_aportadas"] else ""),
        ("Estado validación:", datos["estado_validacion"] or "")
    ]

    entradas = {}

    for i, (label_text, valor) in enumerate(campos):
        col = 0 if i % 2 == 0 else 2
        row = i // 2
        tk.Label(form_frame, text=label_text, bg="white", font=("Arial", 12)).grid(row=row, column=col, sticky="e", pady=5, padx=(10, 5))

        if "Carrera" in label_text:
            entrada = ttk.Combobox(form_frame, values=[c[1] for c in (carreras or [])], font=("Arial", 12), state="readonly")
            entrada.set(valor)
        elif "Voluntariado" in label_text:
            entrada = ttk.Combobox(form_frame, values=[v[1] for v in (voluntariados or [])], font=("Arial", 12), state="readonly")
            entrada.set(valor)
        else:
            if "Contraseña" in label_text:
                entrada = tk.Entry(form_frame, show="*", font=("Arial", 12))
            else:
                entrada = tk.Entry(form_frame, font=("Arial", 12))
            entrada.insert(0, valor)

        entrada.grid(row=row, column=col + 1, pady=5, sticky="w", padx=(5, 10))
        entradas[label_text] = entrada

    
    final_row = (len(campos) + 1) // 2 + 1
    tk.Label(form_frame, text="Datos Voluntariado:", font=("Arial", 12, "bold"),
             bg="white").grid(row=final_row, column=0, columnspan=4, sticky="w", pady=(20, 5), padx=10)

    for i, (label_text, valor) in enumerate(voluntariado_extra):
        row = final_row + i + 1
        tk.Label(form_frame, text=label_text, bg="white", font=("Arial", 12)).grid(row=row, column=0, sticky="e", pady=5, padx=(10, 5))
        entrada = tk.Entry(form_frame, font=("Arial", 12))
        entrada.insert(0, valor)
        entrada.grid(row=row, column=1, pady=5, sticky="w", padx=(5, 10))
        entradas[label_text] = entrada

    
    def guardar_cambios():
        try:
            con = conectar()
            cur = con.cursor()


            cur.execute("""
                UPDATE Usuarios SET
                    nombre=%s, apellido_paterno=%s, apellido_materno=%s,
                    correo=%s, telefono=%s, fecha_registro=%s,
                    usuario=%s, password=%s
                WHERE id=%s
            """, (
                entradas["Nombre:"].get(),
                entradas["Apellido Paterno:"].get(),
                entradas["Apellido Materno:"].get(),
                entradas["Correo:"].get(),
                int(entradas["Teléfono:"].get()),
                entradas["Fecha de registro:"].get(),
                entradas["Usuario:"].get(),
                entradas["Contraseña:"].get(),
                datos["id_usuario"]
            ))

            
            cur.execute("""
                UPDATE Estudiantes SET
                    matricula=%s, id_carrera=%s
                WHERE id_usuario=%s
            """, (
                entradas["Matrícula:"].get(),
                combobox_ids["Carrera"][entradas["Carrera:"].get()],
                datos["id_usuario"]
            ))

            
            cur.execute("""
                UPDATE Voluntariados_Estudiantes SET
                    id_voluntariado=%s,
                    fecha_participacion=%s,
                    horas_aportadas=%s,
                    estado_validacion=%s
                WHERE id_estudiante=%s
            """, (
                combobox_ids["Voluntariado"][entradas["Voluntariado:"].get()],
                entradas["Fecha de participación:"].get() or None,
                int(entradas["Horas Aportadas:"].get() or 0),
                entradas["Estado validación:"].get() or "Pendiente",
                datos["id_usuario"]
            ))

            con.commit()
            con.close()
            messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
            regresar(frame_edit, root, notebook, FONDO_GENERAL, style)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar los cambios:\n{e}")
            if con: con.rollback()
            if con: con.close()

    button_frame = tk.Frame(frame_edit, bg=FONDO_GENERAL)
    button_frame.pack(pady=20)

    ttk.Button(button_frame, text="Guardar Cambios", style="Blue.TButton", command=guardar_cambios).pack(side="left", padx=15)
    tk.Button(button_frame, text="← Regresar", bg="lightgray", command=lambda: regresar(frame_edit, root, notebook, FONDO_GENERAL, style), font=("Arial", 12)).pack(side="left", padx=15)



def regresar(frame_edit, root, notebook, FONDO_GENERAL, style):
    frame_edit.destroy()
    from tab_estudiantes import crear_tab_estudiantes
    crear_tab_estudiantes(root, notebook, FONDO_GENERAL, style)