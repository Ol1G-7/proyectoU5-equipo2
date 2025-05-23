from conexion_bd import conectar
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry
from constantes import FONDO_GENERAL
from estilos import FUENTE_INPUT

def obtener_datos_proyectos():
    conexion = conectar()
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
            CONCAT(IFNULL(dv.calle, ''), ' ', IFNULL(dv.numero, ''), ', ', IFNULL(dv.colonia, '')) AS direccion,
            v.vacantes,
            CASE WHEN v.status = 1 THEN 'Activo' ELSE 'Inactivo' END
        FROM Voluntariados v
        JOIN Tipos_Voluntariados tv ON v.id_tipo = tv.id
        JOIN Responsables r ON v.id_responsable = r.id
        LEFT JOIN Direcciones_Voluntariados dv ON v.id = dv.id_voluntariado
        WHERE v.status = 1
    """)

    resultados = cursor.fetchall()
    conexion.close()

    datos_visibles = []
    textos_extras = {}  

    if resultados is not None:
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
    global notebookPrincipal
    global framePrincipal
    framePrincipal = frame
    notebookPrincipal = notebook
    notebook.add(frame, text="Gestión de Proyectos")
    
    crear_contenido_tab_proyectos(frame)

def crear_contenido_tab_proyectos(frame):
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
            valores = tree.item(item[0], "values")
            id_vol = int(valores[0])

            txt_actividades.delete("1.0", tk.END)
            txt_descripcion.delete("1.0", tk.END)

            txt_actividades.insert(tk.END, textos_extra[id_vol]["actividades"])
            txt_descripcion.insert(tk.END, textos_extra[id_vol]["descripcion"])

    tree.bind("<Double-1>", manejar_click)
    tree.bind("<<TreeviewSelect>>", al_seleccionar_fila)

    
    frame_btns = tk.Frame(frame, bg=FONDO_GENERAL)
    frame_btns.pack(pady=10)

    ttk.Button(frame_btns, text="Agregar ➕", style="Green.TButton",
               command=lambda: mostrar_formulario_voluntariado(frame)).pack(side="left", padx=10)
    ttk.Button(frame_btns, text="Editar 📝", style="Blue.TButton",
               command=lambda: editar_seleccion(tree, frame)).pack(side="left", padx=10)
    ttk.Button(frame_btns, text="Eliminar ❌", style="Red.TButton",
                command=lambda: eliminar_seleccion(tree, frame)).pack(side="left", padx=10)
    ttk.Button(frame_btns, text="Dirección 🏠", style="Yellow.TButton",
              command=lambda: mostrar_direccion_seleccion(tree, frame)).pack(side="left", padx=10)

def mostrar_direccion_seleccion(tree, frame):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un voluntariado primero")
        return
    
    id_voluntariado = tree.item(seleccion)['values'][0]
    mostrar_formulario_direccion(frame, id_voluntariado, 
                               lambda: recargar_pantalla_principal())
    
    
def mostrar_formulario_direccion(frame, id_voluntariado, callback=None):
    limpiar_frame(frame)
    
    municipios = obtener_municipios()
    direccion_existente = obtener_direccion_voluntariado(id_voluntariado)
    
    
    navbar = tk.Frame(frame, bg="#3C88CF", height=60)
    navbar.pack(side="top", fill="x")
    tk.Label(navbar, text="📍", font=("Arial", 24), bg="#3C88CF", fg="white").pack(side="left", padx=20)
    tk.Label(navbar, text="Dirección del Voluntariado", font=("Arial", 14, "bold"),
             bg="#3C88CF", fg="white").pack(side="left")

    
    form_frame = tk.Frame(frame, bg="white", padx=40, pady=30, bd=2, relief="groove")
    form_frame.pack(padx=40, pady=20, fill="x")

    campos = {}
    etiquetas = ["Calle", "Número", "Colonia", "Código Postal", "Municipio", "Referencias"]
    
    for idx, label in enumerate(etiquetas):
        row = idx
        tk.Label(form_frame, text=label + ":", font=FUENTE_INPUT, bg="white").grid(
            row=row, column=0, sticky="e", padx=5, pady=5)
        
        if label == "Municipio":
            combo = ttk.Combobox(form_frame, values=list(municipios.keys()), state="readonly")
            combo.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            campos[label] = combo
        elif label == "Referencias":
            text = tk.Text(form_frame, width=40, height=4, font=FUENTE_INPUT)
            text.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            campos[label] = text
        else:
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            campos[label] = entry

    
    if direccion_existente:
        campos["Calle"].insert(0, direccion_existente[0])
        campos["Número"].insert(0, direccion_existente[1])
        campos["Colonia"].insert(0, direccion_existente[2])
        campos["Código Postal"].insert(0, direccion_existente[3])
        campos["Municipio"].set(direccion_existente[4])
        campos["Referencias"].insert("1.0", direccion_existente[5])

    def guardar_direccion():
        try:
            datos = (
                campos["Calle"].get(),
                int(campos["Número"].get()),
                campos["Colonia"].get(),
                campos["Código Postal"].get(),
                municipios[campos["Municipio"].get()],
                campos["Referencias"].get("1.0", "end").strip()
            )
            
            if guardar_direccion_voluntariado(id_voluntariado, datos):
                messagebox.showinfo("Éxito", "Dirección guardada correctamente")
                if callback:
                    callback()
        except ValueError:
            messagebox.showerror("Error", "El número debe ser un valor entero")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    
    boton_frame = tk.Frame(frame, bg=FONDO_GENERAL)
    boton_frame.pack(pady=20)
    
    ttk.Button(boton_frame, text="Guardar Dirección", style="Green.TButton",
              command=guardar_direccion).pack(side="left", padx=10)
    
    if callback:
        ttk.Button(boton_frame, text="Volver", style="Blue.TButton",
                  command=callback).pack(side="left", padx=10)


def eliminar_seleccion(tree, frame):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un registro para eliminar.")
        return
    datos = tree.item(seleccion)['values']
    confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar voluntariado '{datos[1]}'?")
    if confirmar:
        eliminar_voluntariado(datos[0], frame)

def eliminar_voluntariado(id_v, frame):
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
        cursor = con.cursor()
        cursor.execute("UPDATE Voluntariados SET status = 0 WHERE id = %s", (id_v,))

        con.commit()
        messagebox.showinfo("Éxito", "Voluntariado eliminado correctamente.")
        recargar_pantalla_principal()
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar: {e}")
    finally:
        con.close()

def recargar_pantalla_principal():
    limpiar_frame(framePrincipal)
    crear_contenido_tab_proyectos(framePrincipal)

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def obtener_responsables():
    con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
    cursor = con.cursor()
    cursor.execute("SELECT id, nombre FROM Responsables")
    datos = cursor.fetchall()
    con.close()
    if datos is None:
        return {}
    return {nombre: id_ for id_, nombre in datos}

def obtener_colaboradores():
    con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
    cursor = con.cursor()
    cursor.execute("SELECT id, nombre FROM Colaboradores")
    datos = cursor.fetchall()
    con.close()
    if datos is None:
        return {}
    return {nombre: id_ for id_, nombre in datos}

def obtener_tipos():
    con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
    cursor = con.cursor()
    cursor.execute("SELECT id, nombre FROM Tipos_Voluntariados")
    datos = cursor.fetchall()
    con.close()
    if datos is None:
        return {}
    return {nombre: id_ for id_, nombre in datos}

def insertar_voluntariado(data):
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
        cursor = con.cursor()
        query = """
            INSERT INTO Voluntariados
            (nombre, actividades, objetivo, fecha_inicio, fecha_fin, descripcion, perfil, id_responsable,
            id_colaborador, id_tipo, vacantes, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, data)
        id = cursor.lastrowid
        con.commit()
        return id
    except Exception as e:
        messagebox.showerror("Error", f"Error al insertar: {e}")
        return None
    finally:
        con.close()

def actualizar_voluntariado(id_v, data):
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
        cursor = con.cursor()
        query = """
            UPDATE Voluntariados
            SET nombre=%s, actividades=%s, objetivo=%s, fecha_inicio=%s, fecha_fin=%s,
                descripcion=%s, perfil=%s, id_responsable=%s, id_colaborador=%s, id_tipo=%s,
                vacantes=%s, status=%s
            WHERE id = %s
        """
        cursor.execute(query, data + (id_v,))
        con.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar: {e}")
    finally:
        con.close()

def editar_seleccion(tree, frame):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Atención", "Selecciona un registro para editar.")
        return
    datos = tree.item(seleccion)['values']
    id_voluntariado = datos[0]
    datos_completos = obtener_voluntariado_por_id(id_voluntariado)
    mostrar_formulario_voluntariado(frame, datos_existentes=datos_completos)

def obtener_voluntariado_por_id(id_v):
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
        cursor = con.cursor()
        query = """
            SELECT v.id, v.nombre, v.actividades, v.objetivo, v.fecha_inicio, v.fecha_fin, v.descripcion, v.perfil,
                   r.nombre AS responsable, c.nombre AS colaborador, t.nombre AS tipo, v.vacantes, v.status
            FROM Voluntariados v
            JOIN Responsables r ON v.id_responsable = r.id
            JOIN Colaboradores c ON v.id_colaborador = c.id
            JOIN Tipos_Voluntariados t ON v.id_tipo = t.id
            WHERE v.id = %s
        """
        cursor.execute(query, (id_v,))
        resultado = cursor.fetchone()
        return resultado
    finally:
        con.close()

def mostrar_formulario_voluntariado(frame, datos_existentes=None):
    limpiar_frame(frame)

    campos = {}

    responsables = obtener_responsables()
    colaboradores = obtener_colaboradores()
    tipos = obtener_tipos()

    
    navbar = tk.Frame(frame, bg="#3C88CF", height=60)
    navbar.pack(side="top", fill="x")
    tk.Label(navbar, text="🧩", font=("Arial", 24), bg="#3C88CF", fg="white").pack(side="left", padx=20)
    tk.Label(navbar, text="Agregar/Editar Voluntariado", font=("Arial", 14, "bold"),
             bg="#3C88CF", fg="white").pack(side="left")

    
    form_frame = tk.Frame(frame, bg="white", padx=40, pady=30, bd=2, relief="groove")
    form_frame.pack(padx=40, pady=20, fill="x")

    etiquetas_campos = [
        ("Nombre", tk.Entry),
        ("Actividades", tk.Text),
        ("Objetivo", tk.Entry),
        ("Descripción", tk.Text),
        ("Perfil", tk.Entry),
        ("Responsable", ttk.Combobox),
        ("Colaborador", ttk.Combobox),
        ("Tipo", ttk.Combobox),
        ("Vacantes", tk.Entry),
        ("Status", tk.Entry),
    ]

    
    fila_fecha = tk.Frame(form_frame, bg="white")
    fila_fecha.grid(row=5, column=0, columnspan=4, sticky="w", padx=5, pady=5)

    tk.Label(fila_fecha, text="Fecha Inicio:", font=FUENTE_INPUT, bg="white").pack(side="left", padx=(0, 5))
    fecha_inicio = DateEntry(fila_fecha, width=15, date_pattern='yyyy-mm-dd')
    fecha_inicio.configure(font=FUENTE_INPUT)
    fecha_inicio.pack(side="left", padx=5)

    tk.Label(fila_fecha, text="Fecha Fin:", font=FUENTE_INPUT, bg="white").pack(side="left", padx=(20, 5))
    fecha_fin = DateEntry(fila_fecha, width=15, date_pattern='yyyy-mm-dd')
    fecha_fin.configure(font=FUENTE_INPUT)
    fecha_fin.pack(side="left", padx=5)

    campos["Fecha Inicio"] = fecha_inicio
    campos["Fecha Fin"] = fecha_fin

    for idx, (label, widget_class) in enumerate(etiquetas_campos):
        row, col = divmod(idx, 2)

        tk.Label(form_frame, text=label + ":", font=FUENTE_INPUT, bg="white", anchor="e", width=18).grid(
            row=row, column=col * 2, sticky="e", padx=5, pady=10)

        if widget_class == tk.Entry:
            entry = ttk.Entry(form_frame, width=40, style="Custom.TEntry")
            entry.grid(row=row, column=col * 2 + 1, sticky="w", padx=5, pady=5)
            campos[label] = entry

        elif widget_class == tk.Text:
            text = tk.Text(form_frame, width=35, height=4, font=FUENTE_INPUT, relief="solid", bd=1,
                           bg='white', fg="black", highlightbackground="gray")
            text.grid(row=row, column=col * 2 + 1, sticky="w", padx=5, pady=5)
            campos[label] = text

        elif label in ["Responsable", "Colaborador"]:
            combo = ttk.Combobox(
                form_frame,
                values=list((responsables if label == "Responsable" else colaboradores).keys()),
                state="normal", width=37, style="Custom.TCombobox"
            )
            combo.grid(row=row, column=col * 2 + 1, sticky="w", padx=5, pady=5)
            campos[label] = combo

        elif label == "Tipo":
            combo = ttk.Combobox(
                form_frame,
                values=list(tipos.keys()),
                state="readonly", width=37, style="Custom.TCombobox"
            )
            combo.grid(row=row, column=col * 2 + 1, sticky="w", padx=5, pady=5)
            campos[label] = combo

    if datos_existentes:
        campos["Nombre"].insert(0, datos_existentes[1])
        campos["Actividades"].insert("1.0", datos_existentes[2])
        campos["Objetivo"].insert(0, datos_existentes[3])
        campos["Fecha Inicio"].set_date(datos_existentes[4])
        campos["Fecha Fin"].set_date(datos_existentes[5])
        campos["Descripción"].insert("1.0", datos_existentes[6])
        campos["Perfil"].insert(0, datos_existentes[7])
        campos["Responsable"].set(datos_existentes[8])
        campos["Colaborador"].set(datos_existentes[9])
        campos["Tipo"].set(datos_existentes[10])
        campos["Vacantes"].insert(0, datos_existentes[11])
        campos["Status"].insert(0, datos_existentes[12])

    def guardar():
        try:
            responsable_nombre = campos["Responsable"].get().strip()
            colaborador_nombre = campos["Colaborador"].get().strip()
            tipo_nombre = campos["Tipo"].get()

            if not responsable_nombre or not colaborador_nombre or not tipo_nombre:
                messagebox.showwarning("Campos obligatorios", "Responsable, Colaborador y Tipo son obligatorios.")
                return

            responsable_id = responsables.get(responsable_nombre)
            if not responsable_id:
                con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
                cursor = con.cursor()
                cursor.execute("INSERT INTO Responsables (nombre) VALUES (%s)", (responsable_nombre,))
                con.commit()
                responsable_id = cursor.lastrowid
                con.close()

            colaborador_id = colaboradores.get(colaborador_nombre)
            if not colaborador_id:
                con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
                cursor = con.cursor()
                cursor.execute("INSERT INTO Colaboradores (nombre) VALUES (%s)", (colaborador_nombre,))
                con.commit()
                colaborador_id = cursor.lastrowid
                con.close()

            tipo_id = tipos.get(tipo_nombre)
            if not tipo_id:
                messagebox.showwarning("Tipo inválido", "Selecciona un tipo válido.")
                return

            datos = (
                campos["Nombre"].get(),
                campos["Actividades"].get("1.0", "end").strip(),
                campos["Objetivo"].get(),
                campos["Fecha Inicio"].get(),
                campos["Fecha Fin"].get(),
                campos["Descripción"].get("1.0", "end").strip(),
                campos["Perfil"].get(),
                responsable_id,
                colaborador_id,
                tipo_id,
                campos["Vacantes"].get(),
                campos["Status"].get()
            )

            if any(d == "" or d is None for d in datos):
                messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
                return

            if datos_existentes:
                actualizar_voluntariado(datos_existentes[0], datos)
                messagebox.showinfo("Éxito", "Voluntariado actualizado correctamente.")
                recargar_pantalla_principal()
            else:
                insertar_voluntariado(datos)
                messagebox.showinfo("Éxito", f"Voluntariado guardado exitosamente.")
                recargar_pantalla_principal()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))

   
    boton_frame = tk.Frame(frame, bg=FONDO_GENERAL)
    boton_frame.pack(pady=20)
    ttk.Button(boton_frame, text="Guardar ✅", style="Green.TButton", command=guardar).pack(side="left", padx=15)
    ttk.Button(boton_frame, text="← Volver", style="Blue.TButton",
           command=lambda: recargar_pantalla_principal()).pack(side="left", padx=15)

def obtener_municipios():
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
        cursor = con.cursor()
        cursor.execute("SELECT id, nombre FROM Municipios")
        datos = cursor.fetchall()
        if datos is None:
            return {}
        return {nombre: id_ for id_, nombre in datos}
    finally:
        con.close()

def guardar_direccion_voluntariado(id_voluntariado, datos_direccion):
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
        cursor = con.cursor()
        
        
        cursor.execute("SELECT 1 FROM Direcciones_Voluntariados WHERE id_voluntariado = %s", (id_voluntariado,))
        existe = cursor.fetchone()
        
        if existe:
            query = """
                UPDATE Direcciones_Voluntariados
                SET calle=%s, numero=%s, colonia=%s, cp=%s, id_municipio=%s, referencias=%s
                WHERE id_voluntariado=%s
            """
        else:
            query = """
                INSERT INTO Direcciones_Voluntariados
                (calle, numero, colonia, cp, id_municipio, referencias, id_voluntariado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        
        cursor.execute(query, datos_direccion + (id_voluntariado,))
        con.commit()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar dirección: {e}")
        return False
    finally:
        con.close()

def obtener_direccion_voluntariado(id_voluntariado):
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="", database="TopicosProyectoDB")
        cursor = con.cursor()
        query = """
            SELECT d.calle, d.numero, d.colonia, d.cp, m.nombre AS municipio, d.referencias
            FROM Direcciones_Voluntariados d
            JOIN Municipios m ON d.id_municipio = m.id
            WHERE d.id_voluntariado = %s
        """
        cursor.execute(query, (id_voluntariado,))
        return cursor.fetchone()
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener dirección: {e}")
        return None
    finally:
        con.close()
