from core.display import ScreenController
from ui.themes import COLORS, FONTS, FONT_PATH
from PIL import ImageFont

def main():
    print("Cargando Interfaz de PiScan22...")
    screen = ScreenController()
    
    # 1. Limpiar el lienzo con el color de fondo definido en themes.py (Negro)
    screen.clear(color=COLORS["background"])
    
    # 2. Intentar cargar la fuente retro física
    try:
        font_title = ImageFont.truetype(FONT_PATH, FONTS["title"])
        font_small = ImageFont.truetype(FONT_PATH, FONTS["small"])
    except OSError:
        print("Error: No se encontró la fuente en la ruta especificada.")
        print(f"Ruta buscada: {FONT_PATH}")
        return

    # 3. Dibujar textos en el lienzo (x, y)
    # Título principal
    screen.draw.text((120, 120), "PiScan OS 22", font=font_title, fill=COLORS["primary"])
    
    # Subtítulo pequeño
    screen.draw.text((120, 160), "Sistema Inicializado...", font=font_small, fill=COLORS["text"])
    
    # 4. Empujar todo el lienzo modificado a la memoria RAM y ejecutar el motor C
    screen.push_to_screen()
    
    print("¡Pantalla actualizada! Revisa la LCD.")

if __name__ == "__main__":
    main()