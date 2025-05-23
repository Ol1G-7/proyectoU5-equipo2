import tkinter as tk
from tkinter import ttk
from conexion_bd import obtener_datos_estudiante

def crear_detalle_estudiante(root, notebook, FONDO_GENERAL, style, matricula):
    notebook.pack_forget()

    frame_detalle = tk.Frame(root, bg=FONDO_GENERAL)
    frame_detalle.pack(fill="both", expand=True)

    navbar = tk.Frame(frame_detalle, bg="#3C88CF", height=60)
    navbar.pack(side="top", fill="x")
    tk.Label(navbar, text="🧩", font=("Arial", 24), bg="#3C88CF", fg="white").pack(side="left", padx=20)
    tk.Label(navbar, text="Detalle Registro Estudiante", font=("Arial", 14, "bold"),
             bg="#3C88CF", fg="white").pack(side="left")


    tk.Label(frame_detalle, text="Módulo de Gestión de Estudiantes", font=("Arial", 16, "bold"),
             bg=FONDO_GENERAL).pack(pady=15)


    form_frame = tk.Frame(frame_detalle, bg="white", padx=40, pady=30, bd=2, relief="groove")
    form_frame.pack(padx=30, pady=10)

    datos = obtener_datos_estudiante(matricula)


    datos_principales = [
        ("Nombre:", datos["nombre"]),
        ("Matrícula:", datos["matricula"]),
        ("Apellido Paterno:", datos["apellido_paterno"]),
        ("Carrera:", datos["carrera"]),
        ("Apellido Materno:", datos["apellido_materno"]),
        ("Voluntariado:", datos["voluntariado"] or "Sin asignar"),
        ("Correo:", datos["correo"]),
        ("Teléfono:", str(datos["telefono"])),
        ("Fecha de registro:", str(datos["fecha_registro"])),
        ("Usuario:", datos["usuario"]),
        ("Contraseña:", datos["password"])
    ]

    
    for i, (label, valor) in enumerate(datos_principales):
        col = 0 if i % 2 == 0 else 2
        row = i // 2
        tk.Label(form_frame, text=label, bg="white", anchor="e", width=20, font=("Arial", 12, "bold")).grid(row=row, column=col, sticky="e", pady=5, padx=(10, 5))
        tk.Label(form_frame, text=valor, bg="white", anchor="w", width=30, font=("Arial", 12)).grid(row=row, column=col + 1, sticky="w", padx=(5, 10))

    
    start_row = (len(datos_principales) + 1) // 2 + 1
    tk.Label(form_frame, text="Datos Voluntariado:", font=("Arial", 13, "bold"),
             bg="white").grid(row=start_row, column=0, columnspan=4, sticky="w", pady=(20, 5), padx=10)

    
    datos_voluntariado = [
        ("Fecha de participación:", datos["fecha_participacion"].strftime("%Y-%m-%d") if datos["fecha_participacion"] else "Sin registrar"),
        ("Horas Aportadas:", str(datos["horas_aportadas"]) if datos["horas_aportadas"] else "0"),
        ("Estado validación:", datos["estado_validacion"] or "Pendiente")
    ]

    
    for i, (label, valor) in enumerate(datos_voluntariado):
        tk.Label(form_frame, text=label, bg="white", anchor="e", width=20, font=("Arial", 12, "bold")).grid(
            row=start_row + i + 1, column=0, sticky="e", pady=5, padx=(10, 5))
        tk.Label(form_frame, text=valor, bg="white", anchor="w", width=30, font=("Arial", 12)).grid(
            row=start_row + i + 1, column=1, sticky="w", padx=(5, 10))

    
    def regresar():
        frame_detalle.destroy()
        from tab_estudiantes import crear_tab_estudiantes
        crear_tab_estudiantes(root, notebook, FONDO_GENERAL, style)

    tk.Button(frame_detalle, text="← Regresar", bg="lightgray", font=("Arial", 12), command=regresar).pack(pady=20)