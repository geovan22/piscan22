import os
import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from core.touch import TouchScreen
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def main():
    print("Iniciando PiScan22...")
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    # 1. PANTALLA DE LOGO (El touch aún está apagado por seguridad)
    window.draw_logo()
    screen.push_full_screen() # Esto incluye el bloqueo seguro de 1.5s
    
    # 2. INICIAR TOUCH (El bus SPI ya está estable)
    touch = TouchScreen() 
    
    menu_actual = "Principal"
    
    def refresh_screen(m_actual):
        """Redibuja toda la interfaz de forma segura"""
        screen.clear(color="#000000")
        window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), sys_mon.is_connected(), sys_mon.get_battery())
        window.draw_body(m_actual, MENU_ESTRUCTURA[m_actual])
        window.draw_footer(mensaje="Sistema Activo")
        screen.push_full_screen() # Al terminar esto, el bus queda 100% libre

    # 3. DIBUJAR MENÚ INICIAL
    refresh_screen(menu_actual)
    
    try:
        while True:
            # Como push_full_screen se paraliza hasta terminar de dibujar,
            # aquí podemos leer el táctil sin miedo a corromper la imagen.
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
                            
                        elif opcion["tipo"] == "accion":
                            # Feedback visual temporal
                            screen.clear(color="#000000")
                            window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), sys_mon.is_connected(), sys_mon.get_battery())
                            window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
                            window.draw_footer(mensaje=f"Ejecutando: {opcion['nombre']}")
                            screen.push_full_screen()
                            print(f"[COMANDO LANZADO]: {opcion['comando']}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nApagando...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()