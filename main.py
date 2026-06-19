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
    window.draw_header(cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), connected=sys_mon.is_connected(), battery=sys_mon.get_battery())
    window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
    window.draw_footer(mensaje="Sistema Activo")
    screen.push_full_screen()
    
    try:
        while True:
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
                            screen.clear(color="#000000")
                            window.draw_header(cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), connected=sys_mon.is_connected(), battery=sys_mon.get_battery())
                            window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
                            window.draw_footer(mensaje="Navegando...")
                            screen.push_full_screen()
                            time.sleep(0.5) 
            
            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        print("Apagando...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()