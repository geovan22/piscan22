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
        print("[ERROR] No se encontró splash.bmp")

def main():
    screen = ScreenController()
    sys_mon = SystemMonitor()
    
    # 1. Cargar Splash Screen
    show_splash(screen)
    
    # 2. Iniciar Sistema de Ventanas
    window = MainWindow(screen)
    
    # Estado inicial de la UI
    menu_actual = "Principal"
    opcion_seleccionada = 0
    
    print("Preparando entorno estático...")
    
    # =================================================================
    # OPTIMIZACIÓN: DIBUJAR ELEMENTOS ESTÁTICOS UNA SOLA VEZ
    # =================================================================
    screen.clear(color="#000000")
    window.draw_body(titulo_menu=menu_actual, 
                     lista_opciones=MENU_ESTRUCTURA[menu_actual], 
                     indice_seleccionado=opcion_seleccionada)
    window.draw_footer(mensaje="Sistema Activo y Monitoreando...")
    
    print("Iniciando Bucle de Monitoreo (Solo Header)...")
    
    # 3. BUCLE PRINCIPAL (Solo actualiza los datos que cambian)
    try:
        while True:
            # Leer sensores de hardware reales
            cpu_val = sys_mon.get_cpu()
            ram_val = sys_mon.get_ram()
            temp_val = sys_mon.get_temp()
            net_status = sys_mon.is_connected()
            bat_val = sys_mon.get_battery()
            
            # SOLO dibujamos el Header. 
            # La función draw_header ya pinta un rectángulo gris oscuro en el fondo,
            # lo que borra la hora vieja antes de escribir la nueva, sin tocar el Body.
            window.draw_header(cpu=cpu_val, ram=ram_val, temp=temp_val, connected=net_status, battery=bat_val)
            
            # Enviar fotograma a la pantalla LCD
            screen.push_to_screen()
            
            # Pausa de refresco
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSaliendo de PiScan22...")
        screen.clear(color="#000000")
        screen.push_to_screen()

if __name__ == "__main__":
    main()