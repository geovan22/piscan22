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
    debug_print("MAIN", "=== INICIANDO PISCAN22: CARGA SECTORIZADA SEGURA ===")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen()
    
    # 1. LOGO DE INICIO (Usa full.bmp)
    debug_print("MAIN", "Mostrando Logo...")
    screen.clear(color="#000000")
    window.draw_logo()
    screen.push_full_screen()
    
    # Pausa generosa para que la Pi termine físicamente de pintar el logo.
    time.sleep(4)
    
    # 2. CARGA DEL MENÚ EN BLOQUES (Piezas de Lego)
    # Como usamos header.bmp, body.bmp y footer.bmp, NO tocamos el archivo full.bmp
    # Esto elimina por completo el riesgo de corromper la memoria gráfica.
    menu_actual = "Principal"
    
    def renderizar_y_enviar_menu(menu_name):
        debug_print("MAIN", f"Preparando menú en RAM: {menu_name}")
        screen.clear(color="#000000")
        
        # Dibujar en la RAM de Python
        window.draw_header(
            cpu=sys_mon.get_cpu(), 
            ram=sys_mon.get_ram(), 
            temp=sys_mon.get_temp(), 
            net_type=sys_mon.get_network_type(), 
            battery=sys_mon.get_battery()
        )
        window.draw_body(menu_name, MENU_ESTRUCTURA[menu_name])
        window.draw_footer(mensaje="Sistema Activo")
        
        # Enviar pieza por pieza con tiempos seguros para el motor C
        debug_print("MAIN", "Enviando Header...")
        screen.push_header()
        time.sleep(1.5) # 1.5s garantiza que el bus SPI procese la cabecera
        
        debug_print("MAIN", "Enviando Body...")
        screen.push_body()
        time.sleep(2) # 2.0s para el body porque es el bloque más grande
        
        debug_print("MAIN", "Enviando Footer...")
        screen.push_footer()
        time.sleep(1.5)
        debug_print("MAIN", "Menú cargado al 100%.")

    # Pintar el menú la primera vez en cascada
    renderizar_y_enviar_menu(menu_actual)
    
    # Control del Reloj
    ultimo_minuto = datetime.now().minute
    cmd_file_path = "/dev/shm/piscan_cmd.txt"
    
    debug_print("MAIN", "Bucle principal iniciado (Touch y Reloj activos).")
    
    try:
        while True:
            # A. EVENTO 1: RELOJ INTELIGENTE
            minuto_actual = datetime.now().minute
            if minuto_actual != ultimo_minuto:
                # Comprobamos que el bus SPI esté libre antes de mandar la hora
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

            # B. EVENTO 2: NAVEGACIÓN TÁCTIL
            if not os.path.exists(cmd_file_path):
                pos = touch.get_touch()
                if pos:
                    x, y = pos
                    # Detección del área central (Y: 90 a 280)
                    if 90 < y < 280:
                        indice = int((y - 90) // 45)
                        opciones = MENU_ESTRUCTURA[menu_actual]
                        
                        if 0 <= indice < len(opciones):
                            opcion = opciones[indice]
                            
                            if opcion["tipo"] in ["submenu", "volver"]:
                                menu_actual = opcion["destino"]
                                renderizar_y_enviar_menu(menu_actual)
                            
                            elif opcion["tipo"] == "accion":
                                # Feedback visual rápido en el Footer al ejecutar herramienta
                                debug_print("MAIN", f"Ejecutando comando: {opcion['comando']}")
                                window.draw_footer(mensaje=f"Iniciando: {opcion['nombre']}")
                                screen.push_footer()
                                time.sleep(1.5)
                                # Restaurar mensaje del footer
                                window.draw_footer(mensaje="Sistema Activo")
                                screen.push_footer()

            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando sistema...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()