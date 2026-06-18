import os
import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from PIL import Image
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def main():
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    menu_actual = "Principal"
    opcion_seleccionada = 0
    
    print("Pintando estructura base (Solo habrá un barrido inicial)...")
    
    # 1. Dibujar todo el esqueleto en la RAM de Python
    screen.clear(color="#000000")
    window.draw_header(cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), connected=sys_mon.is_connected(), battery=sys_mon.get_battery())
    window.draw_body(titulo_menu=menu_actual, lista_opciones=MENU_ESTRUCTURA[menu_actual], indice_seleccionado=opcion_seleccionada)
    window.draw_footer(mensaje="Sistema Activo...")
    
    # 2. Enviar la imagen completa por única vez
    screen.push_full_screen()
    
    print("Iniciando reloj en el Header...")
    
    # 3. Bucle de actualización (Solo manda el pedacito del Header)
    try:
        while True:
            # Re-escribimos los datos en la memoria de Python (no afecta la pantalla física aún)
            window.draw_header(
                cpu=sys_mon.get_cpu(), 
                ram=sys_mon.get_ram(), 
                temp=sys_mon.get_temp(), 
                connected=sys_mon.is_connected(), 
                battery=sys_mon.get_battery()
            )
            
            # ¡LA MAGIA! Solo enviamos la tira de 30 píxeles superior
            screen.push_header()
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSaliendo...")

if __name__ == "__main__":
    main()