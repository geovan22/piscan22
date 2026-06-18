# ui/window.py

from datetime import datetime
from PIL import ImageDraw
from ui.themes import COLORS, FONTS, FONT_PATH
from PIL import ImageFont

class MainWindow:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.width
        self.height = screen.height
        
        # Cargar fuentes
        try:
            self.font_main = ImageFont.truetype(FONT_PATH, FONTS["menu"])
            self.font_small = ImageFont.truetype(FONT_PATH, FONTS["small"])
        except:
            self.font_main = ImageFont.load_default()
            self.font_small = ImageFont.load_default()

    def draw_header(self, cpu="0%", ram="0%", temp="0C", connected=False):
        """1. HEADER: Datos del sistema constantes"""
        # Fondo del header (Gris oscuro o verde oscuro)
        self.screen.draw.rectangle((0, 0, self.width, 30), fill="#111111")
        
        # 1.1 Botones de apagado y reset (Iconos simulados con círculos por ahora)
        self.screen.draw.ellipse((5, 5, 25, 25), fill="red")      # Power
        self.screen.draw.ellipse((35, 5, 55, 25), fill="orange")  # Reset
        
        # 1.2 Info de Hardware
        hw_text = f"CPU:{cpu} RAM:{ram} T:{temp}"
        self.screen.draw.text((70, 5), hw_text, font=self.font_small, fill=COLORS["primary"])
        
        # 1.3 Conexión y 1.4 Hora
        hora_actual = datetime.now().strftime("%H:%M")
        estado_red = "ON" if connected else "OFF"
        self.screen.draw.text((self.width - 120, 5), f"NET:{estado_red} {hora_actual}", font=self.font_small, fill="white")
        
        # Línea separadora
        self.screen.draw.line((0, 30, self.width, 30), fill=COLORS["primary"], width=2)

    def draw_body(self, titulo_menu, lista_opciones, indice_seleccionado=0):
        """2. BODY: Menú dinámico"""
        # Título del menú actual
        self.screen.draw.text((10, 40), f"> {titulo_menu}", font=self.font_main, fill="white")
        
        # Dibujar opciones
        y_offset = 80
        for i, opcion in enumerate(lista_opciones):
            texto = f"[{opcion['icono']}] {opcion['nombre']}"
            
            # Resaltar si está seleccionado
            if i == indice_seleccionado:
                self.screen.draw.rectangle((10, y_offset, self.width - 10, y_offset + 30), fill=COLORS["primary"])
                self.screen.draw.text((15, y_offset + 2), texto, font=self.font_main, fill="black")
            else:
                self.screen.draw.text((15, y_offset + 2), texto, font=self.font_main, fill=COLORS["primary"])
                
            y_offset += 40

    def draw_footer(self, mensaje="Listo."):
        """3. FOOTER: Alertas y estado general"""
        # Línea separadora superior del footer
        y_footer = self.height - 30
        self.screen.draw.line((0, y_footer, self.width, y_footer), fill=COLORS["primary"], width=2)
        
        # Texto del footer
        self.screen.draw.text((10, y_footer + 5), f"STATUS: {mensaje}", font=self.font_small, fill="white")