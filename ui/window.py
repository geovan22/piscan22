# ui/window.py

from datetime import datetime
from PIL import ImageDraw, ImageFont
from ui.themes import COLORS, FONTS, FONT_PATH, ICON_FONT_PATH
from ui.menu_config import ICONOS_HEADER

class MainWindow:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.width
        self.height = screen.height
        
        # Cargar fuentes de Texto (Bautizadas como self.font_main y self.font_small)
        try:
            self.font_main = ImageFont.truetype(FONT_PATH, FONTS["menu"])
            self.font_small = ImageFont.truetype(FONT_PATH, FONTS["small"])
        except:
            self.font_main = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            
        # Cargar fuentes de Iconos (Bautizadas como self.icon_main y self.icon_small)
        try:
            self.icon_main = ImageFont.truetype(ICON_FONT_PATH, FONTS["icon_main"])
            self.icon_small = ImageFont.truetype(ICON_FONT_PATH, FONTS["icon_small"])
        except Exception as e:
            print(f"[ALERTA] No se pudo cargar icons.ttf: {e}")
            self.icon_main = self.font_main
            self.icon_small = self.font_small

    def draw_header(self, cpu="0%", ram="0%", temp="0C", connected=False, battery=100):
        """1. HEADER: Datos del sistema y Botones"""
        self.screen.draw.rectangle((0, 0, self.width, 30), fill="#111111")
        
        # Botones Power y Reset
        self.screen.draw.text((8, 5), ICONOS_HEADER["power"], font=self.icon_small, fill=COLORS["danger"])
        self.screen.draw.text((38, 5), ICONOS_HEADER["reset"], font=self.icon_small, fill=COLORS["warning"])
        
        # Info de Hardware
        hw_text = f"CPU:{cpu} RAM:{ram} T:{temp}"
        self.screen.draw.text((70, 5), hw_text, font=self.font_small, fill=COLORS["primary"])
        
        # Estado de Red, Batería y Hora
        fecha_hora = datetime.now().strftime("%d/%m %H:%M")
        icono_red = ICONOS_HEADER["wifi_on"] if connected else ICONOS_HEADER["wifi_off"]
        color_red = COLORS["primary"] if connected else "white"
        
        self.screen.draw.text((self.width - 200, 5), ICONOS_HEADER["battery"], font=self.icon_small, fill=COLORS["primary"])
        self.screen.draw.text((self.width - 175, 5), f"{battery}%", font=self.font_small, fill="white")
        self.screen.draw.text((self.width - 135, 5), icono_red, font=self.icon_small, fill=color_red)
        self.screen.draw.text((self.width - 110, 5), fecha_hora, font=self.font_small, fill="white")
        
        self.screen.draw.line((0, 30, self.width, 30), fill=COLORS["primary"], width=2)

    def draw_body(self, titulo_menu, lista_opciones, indice_seleccionado=0):
        """Dibuja el área central (Y: 30 a 290)"""
        self.screen.draw.rectangle((0, 30, self.width, 290), fill="#000000")
        
        # Título del Menú usando self.font_main
        self.screen.draw.text((15, 40), f"--- {titulo_menu} ---", font=self.font_main, fill=COLORS["primary"])
        
        y_offset = 90
        for i, opcion in enumerate(lista_opciones):
            icono = opcion.get("icono", "")
            nombre = opcion.get("nombre", "")
            indicador = "  >" if opcion["tipo"] == "submenu" else ""
            
            # Dibujar Ícono y Texto usando las fuentes correctas
            self.screen.draw.text((20, y_offset), icono, font=self.icon_main, fill=COLORS["primary"])
            self.screen.draw.text((55, y_offset), f"{nombre}{indicador}", font=self.font_main, fill="white")
            
            y_offset += 45

    def draw_footer(self, mensaje="Listo."):
        """3. FOOTER: Alertas y estado general"""
        y_footer = self.height - 30
        self.screen.draw.line((0, y_footer, self.width, y_footer), fill=COLORS["primary"], width=2)
        self.screen.draw.text((10, y_footer + 5), f"STATUS: {mensaje}", font=self.font_small, fill="white")