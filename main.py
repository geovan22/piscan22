# main.py
import time
from core.config import debug_print
from core.display import ScreenController
from core.system_info import SystemMonitor
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def main():
    debug_print("MAIN", "=== INICIANDO FASE 3: UI COMPLETA Y SECTORIZADA === ")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    # 1. LOGO DE INICIO
    debug_print("MAIN", "Mostrando Logo (ahora con auto-escalado)...")
    screen.clear(color="#000000")
    window.draw_logo()
    screen.push_full_screen()
    time.sleep(3.5) # Pausa para apreciar el logo
    
    # 2. RENDERIZADO INICIAL COMPLETO DE LA UI
    debug_print("MAIN", "Preparando Header, Body y Footer iniciales...")
    menu_actual = "Principal"
    
    # Borramos memoria y dibujamos los 3 bloques en la RAM
    screen.clear(color="#000000")
    window.draw_header(
        cpu=sys_mon.get_cpu(), 
        ram=sys_mon.get_ram(), 
        temp=sys_mon.get_temp(), 
        net_type=sys_mon.get_network_type(), 
        battery=sys_mon.get_battery()
    )
    window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
    window.draw_footer(mensaje="Sistema Activo y Esperando.")
    
    # Mandamos todo junto la primera vez para no ver la carga por partes
    debug_print("MAIN", "Enviando pantalla completa al panel...")
    screen.push_full_screen()
    time.sleep(1)
    
    # 3. BUCLE DE ACTUALIZACIÓN EN TIEMPO REAL
    debug_print("MAIN", "Entrando a bucle de reloj (Solo el Header se repintará)...")
    try:
        while True:
            # Dibujamos SOLO el header en memoria
            window.draw_header(
                cpu=sys_mon.get_cpu(), 
                ram=sys_mon.get_ram(), 
                temp=sys_mon.get_temp(), 
                net_type=sys_mon.get_network_type(), 
                battery=sys_mon.get_battery()
            )
            # Y enviamos SOLO el header por SPI (480x30)
            screen.push_header() 
            
            time.sleep(1) # Actualiza el reloj cada segundo exacto
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando sistema por orden del usuario...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()