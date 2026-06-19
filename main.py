# main.py
import os
import time
from datetime import datetime
from core.config import debug_print
from core.display import ScreenController
from core.system_info import SystemMonitor
from core.touch import TouchScreen
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def main():
    debug_print("MAIN", "=== INICIANDO PISCAN22: MÁXIMA ESTABILIDAD ===")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen()
    
    # 1. LOGO DE INICIO (Usa el archivo full.bmp)
    debug_print("MAIN", "Cargando Logo...")
    screen.clear(color="#000000")
    window.draw_logo()
    screen.push_full_screen()
    
    # PAUSA CRÍTICA: Subimos a 6 segundos. Garantizamos que el demonio
    # termine de leer full.bmp al 100% antes de avanzar.
    time.sleep(6) 
    
    # 2. CARGA DEL MENÚ INICIAL POR SECTORES (Como en la Fase 3)
    menu_actual = "Principal"
    
    def renderizar_y_enviar_menu(menu_name):
        debug_print("MAIN", f"Dibujando menú en RAM: {menu_name}")
        screen.clear(color="#000000")
        
        window.draw_header(
            cpu=sys_mon.get_cpu(), 
            ram=sys_mon.get_ram(), 
            temp=sys_mon.get_temp(), 
            net_type=sys_mon.get_network_type(), 
            battery=sys_mon.get_battery()
        )
        window.draw_body(menu_name, MENU_ESTRUCTURA[menu_name])
        window.draw_footer(mensaje="Sistema Activo")
        
        # Enviamos en cascada usando archivos diferentes (header.bmp, body.bmp, etc.)
        # Así JAMÁS corrompemos el full.bmp del logo.
        debug_print("MAIN", "Enviando Header...")
        screen.push_header()
        time.sleep(1.5)
        
        debug_print("MAIN", "Enviando Body...")
        screen.push_body()
        time.sleep(2.5) # El body requiere más tiempo porque es grande
        
        debug_print("MAIN", "Enviando Footer...")
        screen.push_footer()
        time.sleep(1.5)

    # Pintamos el menú por primera vez
    renderizar_y_enviar_menu(menu_actual)
    
    ultimo_minuto = datetime.now().minute
    cmd_file_path = "/dev/shm/piscan_cmd.txt"
    
    debug_print("MAIN", "Bucle táctil y reloj iniciado.")
    
    try:
        while True:
            # A. RELOJ INTELIGENTE
            minuto_actual = datetime.now().minute
            if minuto_actual != ultimo_minuto:
                if not os.path.exists(cmd_file_path):
                    window.draw_header(
                        cpu=sys_mon.get_cpu(), 
                        ram=sys_mon.get_ram(), 
                        temp=sys_mon.get_temp(), 
                        net_type=sys_mon.get_network_type(), 
                        battery=sys_mon.get_battery()
                    )
                    screen.push_header()
                    time.sleep(1)
                    ultimo_minuto = minuto_actual

            # B. NAVEGACIÓN TÁCTIL
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
                                renderizar_y_enviar_menu(menu_actual)
                            
                            elif opcion["tipo"] == "accion":
                                debug_print("MAIN", f"Comando lanzado: {opcion['comando']}")
                                window.draw_footer(mensaje=f"Iniciando: {opcion['nombre']}")
                                screen.push_footer()
                                time.sleep(1.5)
                                
                                # Simulación de trabajo de la herramienta
                                time.sleep(1.0)
                                
                                window.draw_footer(mensaje="Sistema Activo")
                                screen.push_footer()
                                time.sleep(1.5)

            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando sistema...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()