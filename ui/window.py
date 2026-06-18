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
        
        # Cargar fuentes de Texto
        try:
            self.font_main = ImageFont.truetype(FONT_PATH, FONTS["menu"])
            self.font_small = ImageFont.truetype(FONT_PATH, FONTS["small"])
        except:
            self.font_main = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            
        # Cargar fuentes de Iconos
        try:
            self.icon_main = ImageFont.truetype(ICON_FONT_PATH, FONTS["icon_main"])
            self.icon_small = ImageFont.truetype(ICON_FONT_PATH, FONTS["icon_small"])
        except Exception as e:
            print(f"[ALERTA] No se pudo cargar icons.ttf: {e}")
            self.icon_main = self.font_main
            self.icon_small = self.font_small

    def draw_header(self, cpu="0%", ram="0%", temp="0C", connected=False):
        """1. HEADER: Datos del sistema y Botones"""
        self.screen.draw.rectangle((0, 0, self.width, 30), fill="#111111")
        
        # 1.1 Botones Power y Reset (Ahora son Iconos reales)
        self.screen.draw.text((8, 5), ICONOS_HEADER["power"], font=self.icon_small, fill=COLORS["danger"])
        self.screen.draw.text((38, 5), ICONOS_HEADER["reset"], font=self.icon_small, fill=COLORS["warning"])
        
        # 1.2 Info de Hardware
        hw_text = f"CPU:{cpu} RAM:{ram} T:{temp}"
        self.screen.draw.text((70, 5), hw_text, font=self.font_small, fill=COLORS["primary"])
        
        # 1.3 Conexión y 1.4 Fecha/Hora
        fecha_hora = datetime.now().strftime("%d/%m %H:%M")
        icono_red = ICONOS_HEADER["wifi_on"] if connected else ICONOS_HEADER["wifi_off"]
        color_red = COLORS["primary"] if connected else "white"
        
        # Dibujar icono de red y hora juntos a la derecha
        self.screen.draw.text((self.width - 140, 5), icono_red, font=self.icon_small, fill=color_red)
        self.screen.draw.text((self.width - 110, 5), fecha_hora, font=self.font_small, fill="white")
        
        self.screen.draw.line((0, 30, self.width, 30), fill=COLORS["primary"], width=2)

    def draw_body(self, titulo_menu, lista_opciones, indice_seleccionado=0):
        """2. BODY: Menú dinámico con iconos al lado del texto"""
        self.screen.draw.text((10, 40), f"> {titulo_menu}", font=self.font_main, fill="white")
        
        y_offset = 80
        for i, opcion in enumerate(lista_opciones):
            # Lógica de colores si está seleccionado
            if i == indice_seleccionado:
                self.screen.draw.rectangle((10, y_offset, self.width - 10, y_offset + 30), fill=COLORS["primary"])
                color_texto = COLORS["text_highlight"]
            else:
                color_texto = COLORS["primary"]
                
            # Primero dibujamos el icono con su fuente propia...
            self.screen.draw.text((15, y_offset + 2), opcion['icono'], font=self.icon_main, fill=color_texto)
            
            # ...y luego dibujamos el texto normal justo al lado (+30px a la derecha)
            self.screen.draw.text((45, y_offset + 2), opcion['nombre'], font=self.font_main, fill=color_texto)
                
            y_offset += 40

    def draw_footer(self, mensaje="Listo."):
        """3. FOOTER: Alertas y estado general"""
        y_footer = self.height - 30
        self.screen.draw.line((0, y_footer, self.width, y_footer), fill=COLORS["primary"], width=2)
        self.screen.draw.text((10, y_footer + 5), f"STATUS: {mensaje}", font=self.font_small, fill="white")