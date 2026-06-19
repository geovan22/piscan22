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
    touch = TouchScreen() 
    
    print("Iniciando Interfaz...")
    menu_actual = "Principal"
    
    # Dibujo Inicial
    screen.clear(color="#000000")
    window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), sys_mon.is_connected(), sys_mon.get_battery())
    window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
    screen.push_full_screen()
    
    cmd_file_path = "/dev/shm/piscan_cmd.txt"
    
    try:
        while True:
            # Solo procesar táctil si el archivo de comando NO existe (bus libre)
            if not os.path.exists(cmd_file_path):
                pos = touch.get_touch()
                if pos:
                    x, y = pos
                    if 90 < y < 280:
                        indice = int((y - 90) // 45)
                        opciones = MENU_ESTRUCTURA[menu_actual]
                        
                        if 0 <= indice < len(opciones):
                            opcion = opciones[indice]
                            # Navegación
                            if opcion["tipo"] in ["submenu", "volver"]:
                                menu_actual = opcion["destino"]
                                screen.clear(color="#000000")
                                window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), sys_mon.is_connected(), sys_mon.get_battery())
                                window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
                                screen.push_full_screen()
                                time.sleep(0.5)
            
            time.sleep(0.2) # Pausa mayor para evitar saturación de bus SPI
            
    except KeyboardInterrupt:
        print("Apagando...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()