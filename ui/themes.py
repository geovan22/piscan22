import os

# Determinar la ruta absoluta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ruta de la fuente retro
FONT_PATH = os.path.join(BASE_DIR, "ui", "assets", "fonts", "retro.ttf")

# Paleta de Colores (Estilo Flipper Zero / Terminal Hacker)
COLORS = {
    "background": "#000000",   # Fondo Negro puro
    "primary": "#00FF00",      # Naranja Flipper (o cámbialo a "#00FF00" para Verde Hacker)
    "text": "#FFFFFF",         # Texto Blanco general
    "highlight": "#FF8C00",    # Fondo para el elemento seleccionado
    "text_highlight": "#000000" # Color del texto cuando está seleccionado (Negro)
}

# Tamaños de fuente
FONTS = {
    "title": 32,
    "menu": 24,
    "small": 16
}