import tkinter as tk
from PIL import Image, ImageTk
from constantes import NAVBAR_COLOR, RUTA_LOGO, TEXT_COLOR

def crear_navbar(root, nombre_usuario, home_callback=None, logout_callback=None):
    navbar = tk.Frame(root, bg=NAVBAR_COLOR, height=60)
    navbar.pack(side="top", fill="x")

    try:
        logo_img = Image.open(RUTA_LOGO).resize((40, 40))
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(navbar, image=logo_photo, bg=NAVBAR_COLOR)
        logo_label.image = logo_photo
        logo_label.pack(side="left", padx=15)
    except:
        tk.Label(navbar, text="🧩", font=("Arial", 20), bg=NAVBAR_COLOR, fg=TEXT_COLOR).pack(side="left", padx=20)
    
    for text in ["LOGOUT", nombre_usuario]:
        fg = "black" if text == nombre_usuario else TEXT_COLOR
        command = None

        if text == "LOGOUT":
            command = logout_callback

        if text == nombre_usuario:
            tk.Label(navbar, text=text, bg=NAVBAR_COLOR, fg=fg, font=("Arial", 10, "bold")).pack(side="right", padx=10)
        else:
            if command is not None:
                btn = tk.Button(navbar, text=text, bg=NAVBAR_COLOR, fg=fg, bd=0,
                                font=("Arial", 10, "bold"), command=command)
            else:
                btn = tk.Button(navbar, text=text, bg=NAVBAR_COLOR, fg=fg, bd=0,
                                font=("Arial", 10, "bold"))
            btn.pack(side="right", padx=10)

