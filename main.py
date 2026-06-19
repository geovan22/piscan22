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
    debug_print("MAIN", "=== INICIANDO PISCAN22: SEMÁFORO DE HARDWARE ACTIVO ===")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen()
    
    # 1. LOGO DE INICIO
    debug_print("MAIN", "Cargando Logo...")
    screen.clear(color="#000000")
    window.draw_logo()
    # screen.push_full_screen() ahora pausará el sistema automáticamente por 2.5s
    screen.push_full_screen() 
    
    # 2. CARGA DEL MENÚ SECTORIZADA
    menu_actual = "Principal"
    
    def renderizar_y_enviar_menu(menu_name):
        debug_print("MAIN", f"Preparando menú en RAM: {menu_name}")
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
        
        debug_print("MAIN", "Iniciando ráfaga de envíos. El semáforo los pondrá en cola.")
        # La magia del semáforo: Python no avanzará de línea hasta 
        # que cada bloque esté completamente dibujado en el panel.
        screen.push_header()
        screen.push_body()
        screen.push_footer()
        debug_print("MAIN", "Menú renderizado al 100%.")

    # Primera carga del menú
    renderizar_y_enviar_menu(menu_actual)
    
    # Reloj y Control
    ultimo_minuto = datetime.now().minute
    cmd_file_path = "/dev/shm/piscan_cmd.txt"
    
    debug_print("MAIN", "Bucle principal iniciado (Touch y Reloj activos).")
    
    try:
        while True:
            # A. RELOJ INTELIGENTE
            minuto_actual = datetime.now().minute
            if minuto_actual != ultimo_minuto:
                if not os.path.exists(cmd_file_path):
                    debug_print("MAIN", "Actualizando reloj del Header...")
                    window.draw_header(
                        cpu=sys_mon.get_cpu(), 
                        ram=sys_mon.get_ram(), 
                        temp=sys_mon.get_temp(), 
                        net_type=sys_mon.get_network_type(), 
                        battery=sys_mon.get_battery()
                    )
                    screen.push_header()
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
                                debug_print("MAIN", f"Ejecutando: {opcion['comando']}")
                                window.draw_footer(mensaje=f"Iniciando: {opcion['nombre']}")
                                screen.push_footer()
                                
                                # Simulamos trabajo
                                time.sleep(1.0)
                                
                                window.draw_footer(mensaje="Sistema Activo")
                                screen.push_footer()

            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando sistema...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()