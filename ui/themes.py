# ui/themes.py
import os

# Determinar la ruta absoluta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas de las fuentes
FONT_PATH = os.path.join(BASE_DIR, "ui", "assets", "fonts", "Perfect DOS VGA 437.ttf")
ICON_FONT_PATH = os.path.join(BASE_DIR, "ui", "assets", "fonts", "icons.ttf")

# NUEVA RUTA: Imagen del Logo
SPLASH_PATH = os.path.join(BASE_DIR, "ui", "assets", "images", "splash.bmp")

# Paleta de Colores
COLORS = {
    "background": "#000000",   
    "primary": "#00FF00",      
    "text": "#FFFFFF",         
    "highlight": "#00FF00",    
    "text_highlight": "#000000",
    "danger": "#FF0000",       
    "warning": "#FFA500"       
}

# Tamaños de fuente
FONTS = {
    "title": 32,
    "menu": 24,
    "small": 16,
    "icon_main": 24,  
    "icon_small": 18  
}