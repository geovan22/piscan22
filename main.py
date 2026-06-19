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
    
    # --- PANTALLA DE LOGO ---
    window.draw_logo()
    # Esta línea ahora detendrá Python hasta que el logo esté 100% dibujado
    screen.push_full_screen() 
    time.sleep(1.5) # Dejamos el logo 1.5 segundos para que se vea
    
    menu_actual = "Principal"
    
    def refresh_screen(m_actual):
        """Prepara toda la imagen y la envía al controlador"""
        screen.clear(color="#000000")
        window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), sys_mon.is_connected(), sys_mon.get_battery())
        window.draw_body(m_actual, MENU_ESTRUCTURA[m_actual])
        window.draw_footer(mensaje="Esperando orden...")
        screen.push_full_screen()

    # --- DIBUJAR MENÚ INICIAL ---
    refresh_screen(menu_actual)
    
    try:
        while True:
            # Como push_full_screen bloquea la ejecución mientras se dibuja,
            # aquí estamos 100% seguros de que el bus SPI está libre para el touch.
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
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nApagando...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()