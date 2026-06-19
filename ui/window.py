
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
                pos_x = (self.width - logo_img.width) // 2
                pos_y = (self.height - logo_img.height) // 2
                self.screen.image.paste(logo_img, (pos_x, pos_y))
            else:
                self.draw.rectangle((0, 0, self.width, self.height), fill="#000000")
                self.draw.text((150, 130), ">> PiScan22 <<", font=self.font_main, fill=COLORS["primary"])
        except Exception as e:
            debug_print("WINDOW", f"Fallo imagen: {e}")

    def draw_header(self, cpu="0%", ram="0%", temp="0C", net_type="disconnected", battery=100):
        # Limpiar zona del header
        self.draw.rectangle((0, 0, self.width, 30), fill="#111111")
        
        # 1. Botones (X=5)
        self.draw.text((5, 5), ICONOS_HEADER["power"], font=self.icon_small, fill=COLORS["danger"])
        self.draw.text((28, 5), ICONOS_HEADER["reset"], font=self.icon_small, fill=COLORS["warning"])
        
        # 2. Hardware Info (X=55)
        hw_text = f"CPU:{cpu} RAM:{ram} T:{temp}"
        self.draw.text((55, 6), hw_text, font=self.font_small, fill=COLORS["primary"])
        
        # 3. Batería I2C y Porcentaje (X=235)
        self.draw.text((235, 5), ICONOS_HEADER["battery"], font=self.icon_small, fill=COLORS["primary"])
        self.draw.text((255, 6), f"{battery}%", font=self.font_small, fill="white")
        
        # 4. Estado de Red (X=300)
        color_red = COLORS["primary"]
        if net_type == "wifi":
            icono_red = ICONOS_HEADER["wifi"]
        elif net_type == "lan":
            icono_red = ICONOS_HEADER["lan"]
        else:
            icono_red = ICONOS_HEADER["disconnected"]
            color_red = COLORS["danger"] # Rojo si no hay red
            
        self.draw.text((300, 5), icono_red, font=self.icon_small, fill=color_red)
        
        # 5. Fecha y Hora Formato Completo (X=325)
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.draw.text((325, 6), fecha_hora, font=self.font_small, fill="white")
        
        # 6. Linea divisoria inferior
        self.draw.line((0, 30, self.width, 30), fill=COLORS["primary"], width=2)

    # (MANTÉN AQUÍ TUS FUNCIONES draw_body y draw_footer)
    
    def draw_body(self, titulo_menu, lista_opciones, indice_seleccionado=0):
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
        y_footer = self.height - 30
        self.draw.line((0, y_footer, self.width, y_footer), fill=COLORS["primary"], width=2)
        self.draw.text((10, y_footer + 5), f"STATUS: {mensaje}", font=self.font_small, fill="white")