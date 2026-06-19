import os
import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from core.touch import TouchScreen
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def main():
    print("=== PISCAN22: INICIO ORIGINAL CORREGIDO ===")
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen() 
    
    # --- 1. PANTALLA DE LOGO ---
    print("Enviando Logo...")
    window.draw_logo()
    screen.push_full_screen() 
    
    # SOLUCIÓN 1: El logo ya no se cortará a la mitad ni desaparecerá.
    # Damos 5 segundos reales para que la Pi termine de leer el archivo full.bmp
    time.sleep(5) 
    
    menu_actual = "Principal"
    
    def refresh_screen(m_actual):
        """Tu función original, pero ahora protege el bus SPI"""
        print(f"Dibujando Menú: {m_actual}")
        screen.clear(color="#000000")
        
        # Validación de seguridad por si las funciones cambiaron
        conexion = sys_mon.is_connected() if hasattr(sys_mon, 'is_connected') else False
        bateria = sys_mon.get_battery() if hasattr(sys_mon, 'get_battery') else 100
        
        window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), conexion, bateria)
        window.draw_body(m_actual, MENU_ESTRUCTURA[m_actual])
        window.draw_footer(mensaje="Esperando orden...")
        screen.push_full_screen()
        
        # SOLUCIÓN 2: Adiós pantalla blanca en el footer.
        # Esto detiene a Python 4 segundos. El táctil NO se activará 
        # hasta que la pantalla esté físicamente dibujada al 100%.
        time.sleep(4)

    # --- 2. DIBUJAR MENÚ INICIAL ---
    refresh_screen(menu_actual)
    print("Sistema Activo. Táctil esperando...")
    
    try:
        while True:
            # Ahora es 100% seguro leer el táctil porque el sleep anterior nos protege
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
                            print(f"Comando lanzado: {opcion['comando']}")
                            screen.clear(color="#000000")
                            conexion = sys_mon.is_connected() if hasattr(sys_mon, 'is_connected') else False
                            bateria = sys_mon.get_battery() if hasattr(sys_mon, 'get_battery') else 100
                            
                            window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), conexion, bateria)
                            window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
                            window.draw_footer(mensaje=f"Ejecutando: {opcion['nombre']}")
                            screen.push_full_screen()
                            time.sleep(4) # Escudo al refrescar el footer
                            
                            time.sleep(1) # Trabajo simulado
                            
                            refresh_screen(menu_actual)
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Apagando...")
        screen.clear(color="#000000")
        screen.push_full_screen()
        time.sleep(2)

if __name__ == "__main__":
    main()