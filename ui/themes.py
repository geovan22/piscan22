import os

# Determinar la ruta absoluta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas de las fuentes
FONT_PATH = os.path.join(BASE_DIR, "ui", "assets", "fonts", "Perfect DOS VGA 437.ttf")
ICON_FONT_PATH = os.path.join(BASE_DIR, "ui", "assets", "fonts", "icons.ttf") # ¡NUEVO!

# Paleta de Colores
COLORS = {
    "background": "#000000",   
    "primary": "#00FF00",      # Verde Hacker (o Naranja)
    "text": "#FFFFFF",         
    "highlight": "#00FF00",    
    "text_highlight": "#000000",
    "danger": "#FF0000",       # Rojo para el botón Power
    "warning": "#FFA500"       # Naranja para el botón Reset
}

# Tamaños de fuente
FONTS = {
    "title": 32,
    "menu": 24,
    "small": 16,
    "icon_main": 24,  # Tamaño para iconos en el menú
    "icon_small": 18  # Tamaño para iconos del header
}