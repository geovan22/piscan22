import os
import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from PIL import Image
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def show_splash(screen):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    splash_path = os.path.join(base_dir, "ui", "assets", "images", "splash.bmp")
    
    try:
        splash_img = Image.open(splash_path).resize((screen.width, screen.height))
        screen.image.paste(splash_img, (0, 0))
        screen.push_to_screen() 
        print("Pantalla de inicio cargada. Esperando 5 segundos...")
        time.sleep(5)
    except OSError:
        print(f"[ERROR] No se encontró la imagen en: {splash_path}")

def main():
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    # 1. Mostrar Splash
    show_splash(screen)
    
    menu_actual = "Principal"
    opcion_seleccionada = 0
    
    print("Iniciando Interfaz de Monitoreo...")
    
    try:
        while True:
            # 2. Dibujar todo en la memoria RAM de Python (Súper rápido, no afecta la pantalla física)
            screen.clear(color="#000000")
            window.draw_header(
                cpu=sys_mon.get_cpu(), 
                ram=sys_mon.get_ram(), 
                temp=sys_mon.get_temp(), 
                connected=sys_mon.is_connected(), 
                battery=sys_mon.get_battery()
            )
            window.draw_body(
                titulo_menu=menu_actual, 
                lista_opciones=MENU_ESTRUCTURA[menu_actual], 
                indice_seleccionado=opcion_seleccionada
            )
            window.draw_footer(mensaje="Sistema Activo y Monitoreando...")
            
            # 3. Soltar la bandera. El Daemon C reescribirá la pantalla al instante.
            # Como los píxeles del menú no cambiaron de color, tu ojo solo verá cambiar el reloj.
            screen.push_to_screen()
            
            # Esperar 2 segundos para la próxima lectura real
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSaliendo de PiScan22...")
        screen.clear(color="#000000")
        screen.push_to_screen()
        time.sleep(0.5)

if __name__ == "__main__":
    main()