import tkinter as tk
from tkinter import ttk, messagebox
from constantes import FONDO_GENERAL
from estilos import aplicar_estilos
from navbar import crear_navbar
from tab_horas import crear_tab_horas
from tab_proyectos import crear_tab_proyectos
from tab_reportesProyectos import crear_tab_reportesProyectos
from tab_gestionEstados import iniciar_modulo_estados
from tab_gestionMunicipios import iniciar_modulo_municipios
from tab_gestionTiposVoluntariados import iniciar_modulo_tipos_voluntariados
from tab_gestionColaboradores import iniciar_modulo_colaboradores
from tab_gestionResponsables import iniciar_modulo_responsables
from tab_gestionDepartamentos import iniciar_modulo_departamentos
from tab_gestionCarreras import iniciar_modulo_carreras
from tab_gestionTiposUsuarios import iniciar_modulo_tipos_usuarios
from tab_gestionAdministradores import iniciar_modulo_administradores

class AppAdministrador:
    def __init__(self, root, id_administrador, nombre_administrador):
        self.root = root
        self.id_administrador = id_administrador
        self.nombre_administrador = nombre_administrador

        self.root.title("Sistema de Seguimiento de Voluntariado - Administrador")
        self.root.state('zoomed')
        self.root.config(bg=FONDO_GENERAL)

        self.style = aplicar_estilos(self.root)
        crear_navbar(self.root, nombre_usuario=nombre_administrador, logout_callback=self.logout)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")
        
        self.crear_pestanas()

    def crear_pestanas(self):
        crear_tab_horas(self.root, self.notebook, FONDO_GENERAL, self.style)
        crear_tab_proyectos(self.notebook)
        crear_tab_reportesProyectos(self.notebook)
        #crear_tab_horasE(self.notebook)
        self.crear_tab_gestion_modulos()

    def crear_tab_gestion_modulos(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Gestión de Módulos")

        contenedor = tk.Frame(tab)
        contenedor.pack(fill="both", expand=True)

        sidebar = tk.Frame(contenedor, width=200, bg="#f0f0f0")
        sidebar.pack(side="left", fill="y")

        contenido = tk.Frame(contenedor, bg=FONDO_GENERAL)
        contenido.pack(side="right", fill="both", expand=True)

        def mostrar_modulo(nombre):
            for widget in contenido.winfo_children():
                widget.destroy()
            if nombre == "Estados":
                iniciar_modulo_estados(contenido)
            elif nombre == "Municipios":
                iniciar_modulo_municipios(contenido)
            elif nombre == "Tipos de Voluntariado":
                iniciar_modulo_tipos_voluntariados(contenido)
            elif nombre == "Colaboradores":
                iniciar_modulo_colaboradores(contenido)
            elif nombre == "Responsables":
                iniciar_modulo_responsables(contenido)
            elif nombre == "Departamentos":
                iniciar_modulo_departamentos(contenido)
            elif nombre == "Carreras":
                iniciar_modulo_carreras(contenido)
            elif nombre == "Tipos de Usuario":
                iniciar_modulo_tipos_usuarios(contenido)
            elif nombre == "Administradores":
                iniciar_modulo_administradores(contenido)

        modulos = ["Estados", "Municipios", "Tipos de Voluntariado", "Colaboradores", "Responsables",
                   "Departamentos", "Carreras", "Tipos de Usuario", "Administradores"]
        for modulo in modulos:
            ttk.Button(sidebar, text=modulo, command=lambda m=modulo: mostrar_modulo(m)).pack(fill="x", padx=10, pady=5)

        mostrar_modulo("Estados")  

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
        

if __name__ == "__main__":
    root = tk.Tk()
    AppAdministrador(root, id_administrador=1, nombre_administrador="Admin Demo")
    root.mainloop()
