# ui/window.py
from datetime import datetime
from PIL import ImageDraw, ImageFont
from ui.themes import COLORS, FONTS, FONT_PATH, ICON_FONT_PATH
from ui.menu_config import ICONOS_HEADER
from core.config import debug_print

class MainWindow:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.width
        self.height = screen.height
        
        debug_print("WINDOW", "Cargando fuentes de texto...")
        try:
            self.font_main = ImageFont.truetype(FONT_PATH, FONTS["menu"])
            self.font_small = ImageFont.truetype(FONT_PATH, FONTS["small"])
        except Exception as e:
            debug_print("WINDOW", f"Fallo al cargar fuentes de texto: {e}")
            self.font_main = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            
        debug_print("WINDOW", "Cargando fuentes de iconos...")
        try:
            self.icon_main = ImageFont.truetype(ICON_FONT_PATH, FONTS["icon_main"])
            self.icon_small = ImageFont.truetype(ICON_FONT_PATH, FONTS["icon_small"])
        except Exception as e:
            debug_print("WINDOW", f"Fallo al cargar fuentes de iconos: {e}")
            self.icon_main = self.font_main
            self.icon_small = self.font_small

    @property
    def draw(self):
        return self.screen.draw

    def draw_logo(self):
        """Dibuja la pantalla inicial de arranque"""
        debug_print("WINDOW", "Renderizando Logo en memoria...")
        self.draw.rectangle((0, 0, self.width, self.height), fill="#000000")
        self.draw.text((150, 130), ">> PiScan22 <<", font=self.font_main, fill=COLORS["primary"])
        self.draw.text((170, 170), "Iniciando...", font=self.font_small, fill="white")

    # MANTÉN AQUÍ TUS FUNCIONES draw_header, draw_body, y draw_footer...