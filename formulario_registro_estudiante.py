import tkinter as tk
from tkinter import ttk, messagebox
from conexion_bd import conectar

def crear_formulario_estudiante(root, notebook, FONDO_GENERAL, style):
    notebook.pack_forget()

    frame_form = tk.Frame(root, bg=FONDO_GENERAL)
    frame_form.pack(fill="both", expand=True)

    
    navbar = tk.Frame(frame_form, bg="#3C88CF", height=60)
    navbar.pack(side="top", fill="x")
    tk.Label(navbar, text="🧩", font=("Arial", 24), bg="#3C88CF", fg="white").pack(side="left", padx=20)
    tk.Label(navbar, text="Registrar Estudiante", font=("Arial", 14, "bold"),
             bg="#3C88CF", fg="white").pack(side="left")

    
    tk.Label(frame_form, text="Módulo de Gestión de Estudiantes", font=("Arial", 16, "bold"),
             bg=FONDO_GENERAL).pack(pady=15)

    
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nombre FROM Carreras WHERE status=1")
    carreras = cur.fetchall()
    cur.execute("SELECT id, nombre FROM Voluntariados WHERE status=1")
    voluntariados = cur.fetchall()
    con.close()

    
    form_frame = tk.Frame(frame_form, bg="white", padx=40, pady=30, bd=2, relief="groove")
    form_frame.pack(padx=40, pady=20, fill="x")

    entradas = {}
    combobox_ids = {}

    labels = [
        "Nombre:", "Matrícula:",
        "Apellido Paterno:", "Carrera:",
        "Apellido Materno:", "Voluntariado:",
        "Correo:", "Teléfono:",
        "Fecha de registro:", "Usuario:",
        "Contraseña:"
    ]

    for i, label_text in enumerate(labels):
        col = 0 if i % 2 == 0 else 2
        row = i // 2

        tk.Label(form_frame, text=label_text, bg="white", font=("Arial", 12, "bold"),
                 anchor="e", width=18).grid(row=row, column=col, sticky="e", pady=10, padx=(10, 5))

        if label_text == "Carrera:":
            entrada = ttk.Combobox(form_frame, values=[c[1] for c in carreras], font=("Arial", 12), state="readonly")
            combobox_ids["Carrera"] = {c[1]: c[0] for c in carreras}
        elif label_text == "Voluntariado:":
            entrada = ttk.Combobox(form_frame, values=[v[1] for v in voluntariados], font=("Arial", 12), state="readonly")
            combobox_ids["Voluntariado"] = {v[1]: v[0] for v in voluntariados}
        elif label_text == "Fecha de registro:":
            entrada = tk.Entry(form_frame, font=("Arial", 12))
            entrada.insert(0, "YYYY-MM-DD")
        else:
            entrada = tk.Entry(form_frame, font=("Arial", 12), show="*" if "Contraseña" in label_text else None)

        entrada.grid(row=row, column=col + 1, pady=10, sticky="w", padx=(5, 10), ipadx=30)
        entradas[label_text] = entrada

    
    button_frame = tk.Frame(frame_form, bg=FONDO_GENERAL)
    button_frame.pack(pady=25)

    def registrar_estudiante():
        try:
            con = conectar()
            cur = con.cursor()

            
            cur.execute("""
                INSERT INTO Usuarios (
                    id_tipo_usuario, nombre, apellido_paterno, apellido_materno, 
                    correo, telefono, fecha_registro, usuario, password, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                4, 
                entradas["Nombre:"].get(),
                entradas["Apellido Paterno:"].get(),
                entradas["Apellido Materno:"].get(),
                entradas["Correo:"].get(),
                int(entradas["Teléfono:"].get()),
                entradas["Fecha de registro:"].get(),
                entradas["Usuario:"].get(),
                entradas["Contraseña:"].get(),
                1
            ))

            id_usuario = cur.lastrowid  

            
            cur.execute("""
                INSERT INTO Estudiantes (id_usuario, matricula, id_carrera, status)
                VALUES (%s, %s, %s, %s)
            """, (
                id_usuario,
                entradas["Matrícula:"].get(),
                combobox_ids["Carrera"][entradas["Carrera:"].get()],
                1
            ))

            
            cur.execute("""
                INSERT INTO Voluntariados_Estudiantes (
                    id_estudiante, id_voluntariado, fecha_participacion, horas_aportadas,
                    estado_validacion, observaciones
                ) VALUES (%s, %s, NULL, NULL, NULL, NULL)
            """, (
                id_usuario,
                combobox_ids["Voluntariado"][entradas["Voluntariado:"].get()]
            ))

            con.commit()
            con.close()

            messagebox.showinfo("Éxito", "Estudiante registrado correctamente.")
            regresar(frame_form, root, notebook, FONDO_GENERAL, style)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el estudiante:\n{e}")
            if con: con.rollback()
            if con: con.close()

    ttk.Button(button_frame, text="Registrar Estudiante +", style="Green.TButton", command=registrar_estudiante).pack(side="left", padx=15)
    tk.Button(button_frame, text="← Regresar", bg="lightgray", font=("Arial", 12),
              command=lambda: regresar(frame_form, root, notebook, FONDO_GENERAL, style)).pack(side="left", padx=15)


def regresar(frame_form, root, notebook, FONDO_GENERAL, style):
    frame_form.destroy()
    from tab_estudiantes import crear_tab_estudiantes
    crear_tab_estudiantes(root, notebook, FONDO_GENERAL, style)