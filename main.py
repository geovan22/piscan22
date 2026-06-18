import os
import time
from core.display import ScreenController
from PIL import Image
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def show_splash(screen):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    splash_path = os.path.join(base_dir, "ui", "assets", "images","splash.bmp")
    try:
        splash_img = Image.open(splash_path).resize((screen.width, screen.height))
        screen.image.paste(splash_img, (0, 0))
        screen.push_to_screen()
        print("Pantalla de inicio cargada. Esperando 15 segundos...")
        time.sleep(15) # Espera solicitada
    except OSError:
        print("[ERROR] No se encontró splash.bmp")

def main():
    screen = ScreenController()
    
    # 1. Cargar Splash Screen y esperar
    show_splash(screen)
    
    # 2. Iniciar Sistema de Ventanas
    window = MainWindow(screen)
    
    # Menú inicial a mostrar
    menu_actual = "Principal"
    opcion_seleccionada = 0
    
    print("Iniciando Interfaz Principal...")
    
    # 3. Bucle Principal (Mantiene la UI actualizada)
    # Por ahora corre una vez para pintar la pantalla, luego agregaremos botones físicos/táctiles para que no sea infinito sin control
    try:
        # Limpiar lienzo para quitar el splash
        screen.clear(color="#000000")
        
        # Construir las 3 partes
        # (Aquí pondremos funciones reales de CPU/RAM más adelante, usamos valores fijos por ahora)
        window.draw_header(cpu="12%", ram="45%", temp="42C", connected=False)
        window.draw_body(titulo_menu=menu_actual, 
                         lista_opciones=MENU_ESTRUCTURA[menu_actual], 
                         indice_seleccionado=opcion_seleccionada)
        window.draw_footer(mensaje="Esperando entrada del usuario...")
        
        # Enviar a la pantalla LCD
        screen.push_to_screen()
        
    except KeyboardInterrupt:
        print("Saliendo de PiScan22...")

if __name__ == "__main__":
    main()