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
    window = MainWindow(screen)
    
    show_splash(screen)
    
    menu_actual = "Principal"
    opcion_seleccionada = 0
    mensaje_footer = "Sistema Listo..."
    
    # Control para evitar el barrido constante
    last_update_time = 0
    intervalo_refresco = 30  # Actualiza los datos reales cada 30 segundos
    
    print("Entrando a Bucle Inteligente...")
    
    try:
        while True:
            current_time = time.time()
            
            # Si pasaron 30 segundos (o es la primera vez que arranca)
            if current_time - last_update_time >= intervalo_refresco:
                # 1. Limpiar memoria RAM
                screen.clear(color="#000000")
                
                # 2. Reconstruir los 3 bloques con datos frescos
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
                window.draw_footer(mensaje=mensaje_footer)
                
                # 3. Enviar todo al hardware
                screen.push_to_screen()
                
                last_update_time = current_time
                
            # Pequeña pausa para no quemar el procesador, listo para leer botones luego
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nSaliendo de PiScan22...")
        screen.clear(color="#000000")
        screen.push_to_screen()

if __name__ == "__main__":
    main()