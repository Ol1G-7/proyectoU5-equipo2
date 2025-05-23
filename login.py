import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
from alumnos import AppAlumnos
from administradores import AppAdministrador
from EjecutarScript import setup_base_de_datos


CARPETA_IMAGENES = os.path.join(os.path.dirname(__file__), "imagenes")
RUTA_LOGO = os.path.join(CARPETA_IMAGENES, "escudoITT.png")
RUTA_BIENVENIDA = os.path.join(CARPETA_IMAGENES, "bienvenido.png")
RUTA_PERFIL = os.path.join(CARPETA_IMAGENES, "log1n.png")

COLOR_NAVBAR = "#1A2D80"
COLOR_FONDO = "#ffffff"
FONDO_GENERAL = "#f0f0f0"

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

class LoginVentana:
    def __init__(self, root):
        setup_base_de_datos()
        
        self.root = root
        self.root.title("Login")
        self.root.state('zoomed')
        self.root.config(bg=FONDO_GENERAL)

        self.marco = tk.Frame(self.root, bg=COLOR_FONDO, bd=2, relief="ridge")
        self.marco.pack(expand=True, fill="both", padx=15, pady=15)

        self.crear_navbar()

        self.contenido = tk.Frame(self.marco, bg=COLOR_FONDO)
        self.contenido.pack(expand=True, fill="both")
        self.contenido.rowconfigure(0, weight=1)
        self.contenido.columnconfigure(0, weight=1)

        self.mostrar_login()

    def cargar_imagen(self, ruta, tamaño):
        try:
            imagen = Image.open(ruta)
            imagen = imagen.resize(tamaño, Image.LANCZOS)
            return ImageTk.PhotoImage(imagen)
        except Exception as e:
            print("Error al cargar imagen:", e)
            return None

    def crear_navbar(self):
        navbar = tk.Frame(self.marco, bg=COLOR_NAVBAR, height=60)
        navbar.pack(fill="x", side="top")
        if os.path.exists(RUTA_LOGO):
            try:
                logo_img = Image.open(RUTA_LOGO).resize((40, 40))
                logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(navbar, image=logo_photo, bg=COLOR_NAVBAR)
                logo_label.image = logo_photo
                logo_label.pack(side="left", padx=15)
            except Exception as e:
                print("Error al cargar logo:", e)
                tk.Label(navbar, text="🎓", font=("Arial", 20), bg=COLOR_NAVBAR, fg="white").pack(side="left", padx=15)
        else:
            tk.Label(navbar, text="🎓", font=("Arial", 20), bg=COLOR_NAVBAR, fg="white").pack(side="left", padx=15)

    def mostrar_login(self):
        self.limpiar_formulario()

        central = tk.Frame(self.contenido, bg=COLOR_FONDO)
        central.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        self.contenido.rowconfigure(0, weight=1)
        self.contenido.columnconfigure(0, weight=1)

        tk.Label(central, text="Bienvenido a VoluntariUM", font=("Helvetica", 24, "bold"), bg=COLOR_FONDO, fg="#1A2D80").pack(pady=(10, 5))

        if os.path.exists(RUTA_BIENVENIDA):
            imagen_bienvenida = self.cargar_imagen(RUTA_BIENVENIDA, (120, 120))
            if imagen_bienvenida:
                lbl_img = tk.Label(central, image=imagen_bienvenida, bg=COLOR_FONDO)
                lbl_img.image = imagen_bienvenida
                lbl_img.pack(pady=10)

        login_frame = tk.Frame(central, bg="#f8f8f8", bd=0)
        login_frame.pack(pady=20, ipadx=20, ipady=20)

        estilo_label = {"bg": "#f8f8f8", "fg": "#333", "font": ("Helvetica", 12)}

        tk.Label(login_frame, text="Correo electrónico:", **estilo_label).grid(row=0, column=0, sticky="w", padx=5, pady=(0, 5))
        self.correo_entry = tk.Entry(login_frame, width=30, font=("Helvetica", 12))
        self.correo_entry.grid(row=1, column=0, padx=5, pady=(0, 15))

        tk.Label(login_frame, text="Contraseña:", **estilo_label).grid(row=2, column=0, sticky="w", padx=5, pady=(0, 5))
        self.password_entry = tk.Entry(login_frame, show="*", width=30, font=("Helvetica", 12))
        self.password_entry.grid(row=3, column=0, padx=5, pady=(0, 15))

        btn_login = tk.Button(
            login_frame, text="Iniciar sesión", font=("Helvetica", 12, "bold"),
            bg="#1A2D80", fg="white", relief="flat", width=20,
            command=self.login_action
        )
        btn_login.grid(row=4, column=0, pady=10)
    
    def login_action(self):
        correo = self.correo_entry.get()
        password = self.password_entry.get()
        if not correo or not password:
            messagebox.showwarning("Campos Vacíos", "Por favor completa todos los campos.")
            return

        conn = conectar_mysql()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id, u.nombre, u.password, u.id_tipo_usuario, u.status
            FROM Usuarios u
            WHERE u.correo = %s
        """, (correo,))
        usuario = cursor.fetchone()

        if not usuario or usuario['status'] != 1:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")
            cursor.close()
            conn.close()
            return

        if usuario['password'] != password:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")
            cursor.close()
            conn.close()
            return

        tipo_usuario = usuario['id_tipo_usuario']

        if tipo_usuario == 4:  # Estudiante
            cursor.execute("SELECT id_usuario FROM Estudiantes WHERE id_usuario=%s AND status=1", (usuario['id'],))
            estudiante = cursor.fetchone()
            if estudiante:
                messagebox.showinfo("Acceso", f"¡Bienvenido estudiante {usuario['nombre']}!")
                cursor.close()
                conn.close()
                self.abrir_ventana_estudiante(usuario['id'], usuario['nombre'])
                return
            else:
                messagebox.showerror("Error", "El usuario no está registrado como estudiante activo.")
        elif tipo_usuario == 1:  # Administrador
            cursor.execute("SELECT id_usuario FROM Administradores WHERE id_usuario=%s AND status=1", (usuario['id'],))
            admin = cursor.fetchone()
            if admin:
                messagebox.showinfo("Acceso", f"¡Bienvenido administrador {usuario['nombre']}!")
                cursor.close()
                conn.close()
                self.abrir_ventana_administrador(usuario['id'], usuario['nombre'])
                return
            else:
                messagebox.showerror("Error", "El usuario no está registrado como administrador activo.")
        else:
            messagebox.showerror("Error", "Tipo de usuario no válido.")

        cursor.close()
        conn.close()

    def abrir_ventana_estudiante(self, user_id, nombre):
        self.root.destroy()
        root_estudiante = tk.Tk()
        AppAlumnos(root_estudiante, id_estudiante=user_id, nombre_estudiante=nombre)
        root_estudiante.mainloop()
    
    def abrir_ventana_administrador(self, user_id, nombre):
        self.root.destroy()
        root_administrador = tk.Tk()
        AppAdministrador(root_administrador, id_administrador=user_id, nombre_administrador=nombre)
        root_administrador.mainloop()

    def limpiar_formulario(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    LoginVentana(root)
    root.mainloop()