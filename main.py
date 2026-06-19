# main.py
import os
import time
from datetime import datetime
from core.display import ScreenController
from core.system_info import SystemMonitor
from core.touch import TouchScreen
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def main():
    print("=== INICIANDO PISCAN22: ARQUITECTURA DE ARCHIVOS SEPARADOS ===")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen()
    
    # 1. LOGO DE INICIO
    print("Cargando Logo...")
    screen.clear(color="#000000")
    window.draw_logo()
    screen.push_logo() # Manda logo.bmp
    time.sleep(5) # 5 segundos estrictos para que el bus termine
    
    # 2. CARGA DEL MENÚ INICIAL
    menu_actual = "Principal"
    
    def refresh_full_ui(menu_name):
        print(f"Enviando pantalla completa: Menú {menu_name}")
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
        
        # Manda el menú entero usando menu.bmp. ¡No corrompe el logo!
        screen.push_menu_completo() 
        time.sleep(3) # Pausa segura para que la pantalla termine de dibujar
        print("Menú cargado.")

    # Renderizamos la interfaz la primera vez
    refresh_full_ui(menu_actual)
    
    ultimo_minuto = datetime.now().minute
    cmd_file_path = "/dev/shm/piscan_cmd.txt"
    
    print("Bucle táctil y reloj iniciado.")
    
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
                    screen.push_header() # Usa header.bmp
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
                                print(f"Ejecutando: {opcion['comando']}")
                                window.draw_footer(mensaje=f"Iniciando: {opcion['nombre']}")
                                screen.push_footer()
                                time.sleep(1)
                                
                                # Tiempo en que la herramienta trabaja
                                time.sleep(1.0) 
                                
                                window.draw_footer(mensaje="Sistema Activo")
                                screen.push_footer()
                                time.sleep(1)

            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        print("Apagando...")
        screen.clear(color="#000000")
        screen.push_menu_completo()

if __name__ == "__main__":
    main()