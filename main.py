import os
import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from core.touch import TouchScreen
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def main():
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen() # Bus 0, Device 1
    
    print("Iniciando Interfaz...")
    menu_actual = "Principal"
    
    # Dibujo Inicial
    screen.clear(color="#000000")
    window.draw_header(cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), connected=sys_mon.is_connected(), battery=sys_mon.get_battery())
    window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
    screen.push_full_screen()
    time.sleep(3) # Espera larga para ver si carga
    
    try:
        while True:
            # Solo actualizar reloj si es necesario
            time.sleep(1)
            # Prueba de toque simple
            pos = touch.get_touch()
            if pos:
                print(f"Toque detectado en: {pos}")
            
    except KeyboardInterrupt:
        print("Apagando...")

if __name__ == "__main__":
    main()