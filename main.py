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
    debug_print("MAIN", "=== INICIANDO PISCAN22: SINCRONIZACIÓN PERFECTA ===")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen()
    
    # 1. LOGO DE INICIO AL 100%
    debug_print("MAIN", "Mostrando Logo redimensionado...")
    screen.clear(color="#000000")
    window.draw_logo()
    screen.push_full_screen()
    # LA CLAVE DE LA ESTABILIDAD: 4 segundos para que los cables SPI terminen.
    time.sleep(4) 
    
    # 2. CARGA DEL MENÚ INICIAL
    menu_actual = "Principal"
    
    def refresh_full_ui(menu_name):
        """Dibuja en RAM y manda toda la pantalla de un solo golpe con tiempo seguro."""
        debug_print("MAIN", f"Enviando pantalla completa: Menú {menu_name}")
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
        
        # Enviar todo el bloque a la vez evita que el motor C se coma comandos
        screen.push_full_screen()
        # LA PROTECCIÓN CONTRA PANTALLA BLANCA:
        # Como la pantalla se dibuja de arriba hacia abajo (tarda casi 3s),
        # si Python lee el táctil antes de que termine, colapsa el SPI.
        time.sleep(4) 

    # Pintamos el menú por primera vez
    refresh_full_ui(menu_actual)
    
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
                    # El header es pequeño, con 1 segundo de pausa es suficiente
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
                                refresh_full_ui(menu_actual)
                            
                            elif opcion["tipo"] == "accion":
                                debug_print("MAIN", f"Ejecutando: {opcion['comando']}")
                                window.draw_footer(mensaje=f"Iniciando: {opcion['nombre']}")
                                screen.push_footer()
                                time.sleep(1) # Pausa para que se dibuje el footer seguro
                                
                                # Simulación de la herramienta trabajando
                                time.sleep(1.0)
                                
                                window.draw_footer(mensaje="Sistema Activo")
                                screen.push_footer()
                                time.sleep(1)

            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando sistema...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()