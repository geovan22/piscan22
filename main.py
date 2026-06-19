# main.py - Punto de entrada principal para la aplicación PiScan
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
    
    def refresh_screen(m_actual):
        """Dibuja toda la interfaz en memoria y la envía de una vez"""
        screen.clear(color="#000000")
        window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), sys_mon.is_connected(), sys_mon.get_battery())
        window.draw_body(m_actual, MENU_ESTRUCTURA[m_actual])
        window.draw_footer(mensaje="Sistema Activo")
        screen.push_full_screen()

    # Dibujo Inicial
    refresh_screen(menu_actual)
    
    cmd_file_path = "/dev/shm/piscan_cmd.txt"
    
    try:
        while True:
            if not os.path.exists(cmd_file_path):
                pos = touch.get_touch()
                if pos:
                    x, y = pos
                    if 90 < y < 280:
                        indice = int((y - 90) // 45)
                        opciones = MENU_ESTRUCTURA[menu_actual]
                        
                        if 0 <= indice < len(opciones):
                            opcion = opciones[indice]
                            if opcion["tipo"] in ["submenu", "volver"]:
                                menu_actual = opcion["destino"]
                                refresh_screen(menu_actual)
                                time.sleep(0.5)
            
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        print("Apagando...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()