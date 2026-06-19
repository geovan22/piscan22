# main.py
import time
from core.config import debug_print
from core.display import ScreenController
from core.system_info import SystemMonitor
from ui.window import MainWindow

def main():
    debug_print("MAIN", "=== INICIANDO FASE 2: PRUEBA DE HEADER === ")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    # 1. PANTALLA INICIAL
    debug_print("MAIN", "Mostrando Logo...")
    screen.clear(color="#000000")
    window.draw_logo()
    screen.push_full_screen()
    
    time.sleep(2) # Pausa para ver el logo
    
    # 2. LIMPIAR A NEGRO Y PREPARAR SISTEMA
    screen.clear(color="#000000")
    screen.push_full_screen() # Esto borra el logo de la pantalla
    
    debug_print("MAIN", "Iniciando bucle de reloj en el Header...")
    
    try:
        # Bucle que actualizará SOLO el header cada 1 segundo
        while True:
            window.draw_header(
                cpu=sys_mon.get_cpu(), 
                ram=sys_mon.get_ram(), 
                temp=sys_mon.get_temp(), 
                net_type=sys_mon.get_network_type(), 
                battery=sys_mon.get_battery()
            )
            # Solo mandamos al motor C el pedacito de 480x30
            screen.push_header() 
            
            time.sleep(1) # Esperar un segundo exacto para el reloj
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando sistema...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()