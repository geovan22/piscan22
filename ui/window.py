# ui/window.py
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from ui.themes import COLORS, FONTS, FONT_PATH, ICON_FONT_PATH, SPLASH_PATH
from ui.menu_config import ICONOS_HEADER
from core.config import debug_print

class MainWindow:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.width
        self.height = screen.height
        
        try:
            self.font_main = ImageFont.truetype(FONT_PATH, FONTS["menu"])
            self.font_small = ImageFont.truetype(FONT_PATH, FONTS["small"])
        except Exception:
            self.font_main = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            
        try:
            self.icon_main = ImageFont.truetype(ICON_FONT_PATH, FONTS["icon_main"])
            self.icon_small = ImageFont.truetype(ICON_FONT_PATH, FONTS["icon_small"])
        except Exception:
            self.icon_main = self.font_main
            self.icon_small = self.font_small

    @property
    def draw(self):
        return self.screen.draw

    def draw_logo(self):
        try:
            if os.path.exists(SPLASH_PATH):
                logo_img = Image.open(SPLASH_PATH)
                
                # AUTO-ESCALADO: Obligamos a la imagen a caber en 480x320 
                # manteniendo su proporción sin recortarse.
                logo_img.thumbnail((self.width, self.height))
                
                pos_x = (self.width - logo_img.width) // 2
                pos_y = (self.height - logo_img.height) // 2
                self.screen.image.paste(logo_img, (pos_x, pos_y))
            else:
                self.draw.rectangle((0, 0, self.width, self.height), fill="#000000")
                self.draw.text((150, 130), ">> PiScan22 <<", font=self.font_main, fill=COLORS["primary"])
        except Exception as e:
            debug_print("WINDOW", f"Fallo al procesar imagen: {e}")

    def draw_header(self, cpu="0%", ram="0%", temp="0C", net_type="disconnected", battery=100):
        self.draw.rectangle((0, 0, self.width, 30), fill="#111111")
        self.draw.text((5, 5), ICONOS_HEADER["power"], font=self.icon_small, fill=COLORS["danger"])
        self.draw.text((28, 5), ICONOS_HEADER["reset"], font=self.icon_small, fill=COLORS["warning"])
        
        hw_text = f"CPU:{cpu} RAM:{ram} T:{temp}"
        self.draw.text((55, 6), hw_text, font=self.font_small, fill=COLORS["primary"])
        
        self.draw.text((260, 5), ICONOS_HEADER["battery"], font=self.icon_small, fill=COLORS["primary"])
        self.draw.text((280, 6), f"{battery}%", font=self.font_small, fill="white")
        
        color_red = COLORS["primary"]
        if net_type == "wifi":
            icono_red = ICONOS_HEADER["wifi"]
        elif net_type == "lan":
            icono_red = ICONOS_HEADER["lan"]
        else:
            icono_red = ICONOS_HEADER["disconnected"]
            color_red = COLORS["danger"]
            
        self.draw.text((325, 5), icono_red, font=self.icon_small, fill=color_red)
        
        fecha_hora = datetime.now().strftime("%d/%m %H:%M")
        self.draw.text((350, 6), fecha_hora, font=self.font_small, fill="white")
        self.draw.line((0, 30, self.width, 30), fill=COLORS["primary"], width=2)

    def draw_body(self, titulo_menu, lista_opciones, indice_seleccionado=0):
        # Limita rigurosamente el dibujo a la zona Y: 30 a 290
        self.draw.rectangle((0, 30, self.width, 290), fill="#000000")
        self.draw.text((15, 40), f"--- {titulo_menu} ---", font=self.font_main, fill=COLORS["primary"])
        y_offset = 90
        for i, opcion in enumerate(lista_opciones):
            icono = opcion.get("icono", "")
            nombre = opcion.get("nombre", "")
            indicador = "  >" if opcion["tipo"] == "submenu" else ""
            self.draw.text((20, y_offset), icono, font=self.icon_main, fill=COLORS["primary"])
            self.draw.text((55, y_offset), f"{nombre}{indicador}", font=self.font_main, fill="white")
            y_offset += 45

    def draw_footer(self, mensaje="Listo."):
        # Limita rigurosamente el dibujo a la zona Y: 290 a 320
        self.draw.rectangle((0, 290, self.width, 320), fill="#111111")
        self.draw.line((0, 290, self.width, 290), fill=COLORS["primary"], width=2)
        self.draw.text((10, 298), f"STATUS: {mensaje}", font=self.font_small, fill="white")