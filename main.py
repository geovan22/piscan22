# main.py
import time
from core.config import debug_print
from core.display import ScreenController
from core.system_info import SystemMonitor
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def main():
    debug_print("MAIN", "=== INICIANDO FASE 3: UI SECTORIZADA ===")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    # 1. LOGO DE INICIO AL 100%
    debug_print("MAIN", "Mostrando Logo redimensionado...")
    screen.clear(color="#000000")
    window.draw_logo()
    screen.push_full_screen()
    time.sleep(3.5) # Pausa para apreciar el logo
    
    # 2. RENDERIZADO DEL MENÚ A LA MEMORIA
    debug_print("MAIN", "Dibujando UI en la RAM...")
    menu_actual = "Principal"
    
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
    
    # 3. ENVÍO SECTOR POR SECTOR (ESTO ELIMINA EL "SANGRADO" DEL LOGO)
    debug_print("MAIN", "Enviando Header...")
    screen.push_header()
    time.sleep(0.5)
    
    debug_print("MAIN", "Enviando Body...")
    screen.push_body()
    time.sleep(0.5)
    
    debug_print("MAIN", "Enviando Footer...")
    screen.push_footer()
    time.sleep(0.5)
    
    # 4. BUCLE DE ACTUALIZACIÓN EN TIEMPO REAL
    debug_print("MAIN", "Entrando a bucle de reloj (Solo se refresca el Header)...")
    try:
        while True:
            window.draw_header(
                cpu=sys_mon.get_cpu(), 
                ram=sys_mon.get_ram(), 
                temp=sys_mon.get_temp(), 
                net_type=sys_mon.get_network_type(), 
                battery=sys_mon.get_battery()
            )
            screen.push_header() 
            time.sleep(1) 
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando sistema por orden del usuario...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()