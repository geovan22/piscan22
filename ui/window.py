# ui/window.py
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from ui.themes import COLORS, FONTS, FONT_PATH, ICON_FONT_PATH, SPLASH_PATH
from ui.menu_config import ICONOS_HEADER


class MainWindow:
    """
    Dibuja los tres componentes visuales de la UI en el canvas del ScreenController.
    Cada método dibuja SOLO su región, sin tocar el resto del canvas.
    
    Flujo típico:
        window.draw_header(...)  →  screen.push_header()
        window.draw_body(...)    →  screen.push_body()
        window.draw_footer(...)  →  screen.push_footer()
    
    O para refrescar todo de golpe:
        window.draw_all(...)     →  screen.push_full_screen()
    """

    # Coordenadas Y de cada región (deben coincidir con ScreenController)
    HEADER_Y0 = 0
    HEADER_Y1 = 32
    BODY_Y0   = 32
    BODY_Y1   = 290
    FOOTER_Y0 = 290
    FOOTER_Y1 = 320

    def __init__(self, screen):
        self.screen = screen
        self.width  = screen.width
        self.height = screen.height

        # Fuente de texto
        try:
            self.font_main  = ImageFont.truetype(FONT_PATH, FONTS["menu"])
            self.font_small = ImageFont.truetype(FONT_PATH, FONTS["small"])
        except Exception:
            self.font_main  = ImageFont.load_default()
            self.font_small = ImageFont.load_default()

        # Fuente de íconos (FontAwesome)
        try:
            self.icon_main  = ImageFont.truetype(ICON_FONT_PATH, FONTS["icon_main"])
            self.icon_small = ImageFont.truetype(ICON_FONT_PATH, FONTS["icon_small"])
        except Exception:
            self.icon_main  = self.font_main
            self.icon_small = self.font_small

    @property
    def draw(self):
        return self.screen.draw

    # ------------------------------------------------------------------
    # Logo / Splash
    # ------------------------------------------------------------------

    def draw_logo(self):
        """
        Dibuja el splash en el canvas completo.
        Después llamar a screen.push_full_screen().
        """
        self.screen.clear("black")
        try:
            if os.path.exists(SPLASH_PATH):
                logo = Image.open(SPLASH_PATH).convert("RGB")
                logo = logo.resize((self.width, self.height), Image.LANCZOS)
                self.screen.image.paste(logo, (0, 0))
            else:
                self.draw.text(
                    (100, 140), ">> PiScan22 <<",
                    font=self.font_main, fill=COLORS["primary"]
                )
        except Exception as e:
            # Si falla la imagen, texto de fallback
            self.draw.text((80, 140), f"PiScan22 - Error logo: {e}",
                           font=self.font_small, fill=COLORS["danger"])

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------

    def draw_header(self, cpu="0%", ram="0%", temp="0C",
                    net_type="disconnected", battery=100):
        """
        Dibuja el header (y=0..31) sobre el canvas.
        net_type: 'wifi' | 'lan' | 'disconnected'
        """
        y0, y1 = self.HEADER_Y0, self.HEADER_Y1

        # Fondo del header
        self.draw.rectangle([0, y0, self.width - 1, y1 - 1], fill="#111111")

        # --- Íconos de acción (izquierda) ---
        ic_power = ICONOS_HEADER.get("power", "P")
        ic_reset = ICONOS_HEADER.get("reset", "R")
        self.draw.text((5,  y0 + 5), ic_power, font=self.icon_small, fill=COLORS["danger"])
        self.draw.text((28, y0 + 5), ic_reset,  font=self.icon_small, fill=COLORS["warning"])

        # --- Stats de hardware ---
        hw_text = f"C:{cpu} R:{ram} T:{temp}"
        self.draw.text((55, y0 + 7), hw_text, font=self.font_small, fill=COLORS["primary"])

        # --- Batería ---
        ic_batt = ICONOS_HEADER.get("battery", "B")
        self.draw.text((245, y0 + 5), ic_batt,        font=self.icon_small, fill=COLORS["primary"])
        self.draw.text((265, y0 + 7), f"{battery}%",  font=self.font_small, fill="white")

        # --- Red ---
        if net_type == "wifi":
            ic_red    = ICONOS_HEADER.get("wifi", "\uf1eb")
            color_red = COLORS["primary"]
        elif net_type == "lan":
            ic_red    = ICONOS_HEADER.get("lan", "\uf6ff")
            color_red = COLORS["primary"]
        else:
            ic_red    = ICONOS_HEADER.get("disconnected", "\uf127")
            color_red = COLORS["danger"]

        self.draw.text((315, y0 + 5), ic_red, font=self.icon_small, fill=color_red)

        # --- Fecha y hora ---
        fecha_hora = datetime.now().strftime("%d/%m/%y %H:%M")
        self.draw.text((345, y0 + 7), fecha_hora, font=self.font_small, fill="white")

        # Línea separadora inferior
        self.draw.line([0, y1 - 1, self.width, y1 - 1],
                       fill=COLORS["primary"], width=2)

    # ------------------------------------------------------------------
    # Body
    # ------------------------------------------------------------------

    def draw_body(self, titulo_menu, lista_opciones, indice_seleccionado=0):
        """
        Dibuja el body (y=32..289) sobre el canvas.
        Soporta hasta ~5 opciones con espaciado de 44px.
        """
        y0, y1 = self.BODY_Y0, self.BODY_Y1

        # Fondo del body
        self.draw.rectangle([0, y0, self.width - 1, y1 - 1], fill="#000000")

        # Título del menú actual
        self.draw.text((15, y0 + 8), f"--- {titulo_menu} ---",
                       font=self.font_main, fill=COLORS["primary"])

        # Lista de opciones
        y_item = y0 + 50
        for i, opcion in enumerate(lista_opciones):
            icono  = opcion.get("icono", "")
            nombre = opcion.get("nombre", "")
            # Indicador visual para submenús
            sufijo = "  >" if opcion.get("tipo") == "submenu" else ""

            # Resaltar opción seleccionada
            if i == indice_seleccionado:
                self.draw.rectangle(
                    [0, y_item - 2, self.width - 1, y_item + 40],
                    fill=COLORS["highlight"]
                )
                color_texto = COLORS["text_highlight"]
            else:
                color_texto = "white"

            self.draw.text((18, y_item + 2), icono,
                           font=self.icon_main, fill=COLORS["primary"])
            self.draw.text((52, y_item + 5), f"{nombre}{sufijo}",
                           font=self.font_main, fill=color_texto)

            y_item += 44

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------

    def draw_footer(self, mensaje="Listo."):
        """Dibuja el footer (y=290..319) sobre el canvas."""
        y0, y1 = self.FOOTER_Y0, self.FOOTER_Y1

        self.draw.rectangle([0, y0, self.width - 1, y1 - 1], fill="#111111")
        self.draw.line([0, y0, self.width, y0], fill=COLORS["primary"], width=2)
        self.draw.text((10, y0 + 6), f"STATUS: {mensaje}",
                       font=self.font_small, fill="white")

    # ------------------------------------------------------------------
    # Helpers compuestos
    # ------------------------------------------------------------------

    def draw_all(self, titulo_menu, lista_opciones,
                 cpu="0%", ram="0%", temp="0C",
                 net_type="disconnected", battery=100,
                 mensaje="Listo.", indice_seleccionado=0):
        """Dibuja los tres componentes de una sola vez sobre el canvas."""
        self.screen.clear("black")
        self.draw_header(cpu, ram, temp, net_type, battery)
        self.draw_body(titulo_menu, lista_opciones, indice_seleccionado)
        self.draw_footer(mensaje)