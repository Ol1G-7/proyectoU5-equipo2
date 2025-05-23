from tkinter import ttk
from constantes import BTN_GREEN, BTN_RED, BTN_BLUE

def aplicar_estilos(root):
    style = ttk.Style(root)
    style.theme_use('default')

    # Pestañas
    style.configure('TNotebook.Tab', padding=[10, 5], font=('Segoe UI', 10, 'bold'))

    # Encabezado tabla
    style.configure("Custom.Treeview.Heading",
                    background="#2c3e50",
                    foreground="white",
                    font=('Segoe UI', 10, 'bold'),
                    borderwidth=1,
                    relief="ridge")

    # Cuerpo de tabla
    style.configure("Custom.Treeview",
                    background="#f0f4f7",
                    foreground="black",
                    rowheight=30,
                    fieldbackground="#a2a7ab",
                    font=('Segoe UI', 10),
                    borderwidth=1,
                    relief="solid")

    style.map("Custom.Treeview",
              background=[('selected', '#2980b9')],
              foreground=[('selected', 'white')])

    # Botones Verdes
    style.configure("Green.TButton", font=('Segoe UI', 10, 'bold'), padding=6,
                    background=BTN_GREEN, foreground="white", borderwidth=2)
    style.map("Green.TButton", background=[("active", "#218838")])

    # Botones Rojos
    style.configure("Red.TButton", font=('Segoe UI', 10, 'bold'), padding=6,
                    background=BTN_RED, foreground="white", borderwidth=2)
    style.map("Red.TButton", background=[("active", "#c82333")])

    # Botones Azules
    style.configure("Blue.TButton", font=('Segoe UI', 10, 'bold'), padding=6,
                    background=BTN_BLUE, foreground="white", borderwidth=2)
    style.map("Blue.TButton", background=[("active", "#0069d9")])

    #BOton amarillo

    style.configure("Yellow.TButton", font=('Segoe UI', 10, 'bold'), padding=6,
                background="#ffc107", foreground="black", borderwidth=2)
    style.map("Yellow.TButton", background=[("active", "#e0a800")])

    return style  # ✅ NECESARIO para que lo uses luego

# estilos.py
FONDO_GENERAL = "#f7f9fc"
FUENTE_TITULO = ("Segoe UI", 14, "bold")
FUENTE_ETIQUETA = ("Segoe UI", 10)
FUENTE_INPUT = ("Segoe UI", 10)
COLOR_BOTON = "#4caf50"
COLOR_TEXTO_BLANCO = "#ffffff"
BORDES = 12
