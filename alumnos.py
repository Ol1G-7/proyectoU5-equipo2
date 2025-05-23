import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
from tab_reporteEstudiante import crear_tab_horasE


def conectar_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {err}")
        return None

class AppAlumnos:
    NAVBAR_COLOR = "#1A2D80"
    FONDO_COLOR = "#ffffff"
    TITLE_FONT = ("Arial", 13, "bold")
    SUBTITLE_FONT = ("Arial", 10)
    BTN_FONT = ("Arial", 10)
    TAB_FONT = ("Arial", 10, "bold")

    def __init__(self, root, id_estudiante, nombre_estudiante):
        self.root = root
        self.id_estudiante = id_estudiante
        self.nombre_estudiante = nombre_estudiante
        self.root.title("Sistema de Seguimiento de Voluntariado - Estudiante")
        self.root.state('zoomed')
        self.root.config(bg=self.FONDO_COLOR)
        self.crear_navbar()
        self.crear_pestanas()

    def crear_navbar(self):
        navbar = tk.Frame(self.root, bg=self.NAVBAR_COLOR, height=40)
        navbar.pack(side="top", fill="x")

        ruta_logo = os.path.join(os.path.dirname(__file__), "imagenes", "escudoITT.png")
        try:
            logo_img = Image.open(ruta_logo).resize((28, 28))
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(navbar, image=logo_photo, bg=self.NAVBAR_COLOR)
            logo_label.image = logo_photo
            logo_label.pack(side="left", padx=8, pady=4)
        except:
            tk.Label(navbar, text="🎓", font=("Arial", 14), bg=self.NAVBAR_COLOR, fg="white").pack(side="left", padx=8)

        # Botón de logout a la derecha
        btn_logout = tk.Button(navbar, text="Cerrar sesión", bg="#d9534f", fg="white",
                               font=("Arial", 9, "bold"), command=self.logout)
        btn_logout.pack(side="right", padx=8, pady=4)

        tk.Label(navbar, text=f"👤 {self.nombre_estudiante}", font=("Arial", 10, "bold"),
                 bg=self.NAVBAR_COLOR, fg="white").pack(side="right", padx=8)

        tk.Label(navbar, text="Panel de Alumno", font=("Arial", 11, "bold"),
                 bg=self.NAVBAR_COLOR, fg="white").pack(side="top", pady=2)

    def logout(self):
        self.root.destroy()
        root_login = tk.Tk()
        try:
            from login import LoginVentana
        except ImportError:
            messagebox.showerror("Error", "No se pudo importar LoginVentana.")
            root_login.destroy()
            return
        LoginVentana(root_login)
        root_login.mainloop()

    def crear_pestanas(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', font=self.TAB_FONT, padding=[5, 2])
        style.configure('TNotebook', background=self.FONDO_COLOR, borderwidth=0)
        style.configure('TFrame', background=self.FONDO_COLOR)

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=5, pady=5)

        frame_inscribir = ttk.Frame(notebook)
        frame_registrar = ttk.Frame(notebook)
        crear_tab_horasE(notebook, self.id_estudiante)

        notebook.add(frame_inscribir, text="Inscribirse")
        notebook.add(frame_registrar, text="Registrar Horas")

        for frame in (frame_inscribir, frame_registrar):
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)

        self.crear_tab_inscribir(frame_inscribir)
        self.crear_tab_registrar(frame_registrar)

    def crear_tab_inscribir(self, frame):
        container = tk.Frame(frame, bg=self.FONDO_COLOR)
        container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        container.columnconfigure(0, weight=1)

        tk.Label(container, text="Inscribirse a un voluntariado", font=self.TITLE_FONT, bg=self.FONDO_COLOR).pack(pady=6)
        self.combo_voluntariado = ttk.Combobox(container, width=32, state="readonly", font=self.BTN_FONT)
        self.combo_voluntariado.pack(pady=6, fill="x")
        self.cargar_voluntariados_disponibles()
        ttk.Button(container, text="Inscribirse", command=self.inscribirse_voluntariado).pack(pady=6)

    def cargar_voluntariados_disponibles(self):
        conn = conectar_mysql()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, v.nombre
            FROM Voluntariados v
            WHERE v.status=1 AND v.id NOT IN (
                SELECT id_voluntariado FROM Voluntariados_Estudiantes WHERE id_estudiante=%s
            )
        """, (self.id_estudiante,))
        voluntariados = cursor.fetchall()
        cursor.close()
        conn.close()
        self.combo_voluntariado['values'] = [f"{v[0]} - {v[1]}" for v in voluntariados]

    def inscribirse_voluntariado(self):
        voluntariado = self.combo_voluntariado.get()
        if not voluntariado:
            messagebox.showwarning("Faltan datos", "Selecciona un voluntariado.")
            return
        id_voluntariado = int(voluntariado.split(" - ")[0])
        conn = conectar_mysql()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Voluntariados_Estudiantes (id_estudiante, id_voluntariado, estado_validacion)
            VALUES (%s, %s, 'pendiente')
        """, (self.id_estudiante, id_voluntariado))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Inscripción realizada correctamente.")
        self.cargar_voluntariados_disponibles()

    def crear_tab_registrar(self, frame):
        container = tk.Frame(frame, bg=self.FONDO_COLOR)
        container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        container.columnconfigure(0, weight=1)

        tk.Label(container, text="Registrar horas", font=self.TITLE_FONT, bg=self.FONDO_COLOR).pack(pady=6)
        self.combo_mis_voluntariados = ttk.Combobox(container, width=32, state="readonly", font=self.BTN_FONT)
        self.combo_mis_voluntariados.pack(pady=6, fill="x")
        self.cargar_mis_voluntariados()
        tk.Label(container, text="Fecha:", font=self.SUBTITLE_FONT, bg=self.FONDO_COLOR).pack(pady=2)
        self.fecha_entry = DateEntry(container, width=15, date_pattern='yyyy-mm-dd', font=self.BTN_FONT)
        self.fecha_entry.pack(pady=2)
        tk.Label(container, text="Horas:", font=self.SUBTITLE_FONT, bg=self.FONDO_COLOR).pack(pady=2)
        self.horas_entry = tk.Entry(container, width=15, font=self.BTN_FONT)
        self.horas_entry.pack(pady=2)
        ttk.Button(container, text="Registrar", command=self.registrar_horas).pack(pady=6)

    def cargar_mis_voluntariados(self):
        conn = conectar_mysql()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, v.nombre
            FROM Voluntariados v
            JOIN Voluntariados_Estudiantes ve ON v.id = ve.id_voluntariado
            WHERE ve.id_estudiante=%s
        """, (self.id_estudiante,))
        mis_voluntariados = cursor.fetchall()
        cursor.close()
        conn.close()
        self.combo_mis_voluntariados['values'] = [f"{v[0]} - {v[1]}" for v in mis_voluntariados]

    def registrar_horas(self):
        voluntariado = self.combo_mis_voluntariados.get()
        if not voluntariado:
            messagebox.showwarning("Faltan datos", "Selecciona un voluntariado.")
            return
        id_voluntariado = int(voluntariado.split(" - ")[0])
        fecha = self.fecha_entry.get()
        horas = self.horas_entry.get()
        if not horas.isdigit() or int(horas) <= 0:
            messagebox.showwarning("Faltan datos", "Ingresa un número válido de horas.")
            return

        conn = conectar_mysql()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Voluntariados_Estudiantes
            SET fecha_participacion=%s, horas_aportadas=%s, estado_validacion='pendiente'
            WHERE id_estudiante=%s AND id_voluntariado=%s
        """, (fecha, int(horas), self.id_estudiante, id_voluntariado))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Horas registradas correctamente.")
        self.horas_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    AppAlumnos(root, id_estudiante=1, nombre_estudiante="Juan Pérez")
    root.mainloop()
