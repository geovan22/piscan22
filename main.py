# main.py
import os
import time
from datetime import datetime
from core.display import ScreenController
from core.system_info import SystemMonitor
from core.touch import TouchScreen
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

# Funciones defensivas para evitar colapsos por cambios de versión
def get_net_status(sys_monitor):
    if hasattr(sys_monitor, 'get_network_type'):
        return sys_monitor.get_network_type()
    elif hasattr(sys_monitor, 'is_connected'):
        return "wifi" if sys_monitor.is_connected() else "disconnected"
    return "disconnected"

def get_batt_status(sys_monitor):
    return sys_monitor.get_battery() if hasattr(sys_monitor, 'get_battery') else 100

def main():
    print("=== PISCAN22: INICIANDO SISTEMA BLINDADO ===")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen()
    
    # 1. PANTALLA DE LOGO
    print("Enviando Logo...")
    window.draw_logo()
    screen.push_full_screen(filename="logo.bmp")
    time.sleep(4) # Escudo de tiempo para el bus SPI
    
    menu_actual = "Principal"
    
    def refresh_screen(m_actual):
        """Prepara y envía la interfaz en un solo bloque seguro"""
        screen.clear(color="#000000")
        window.draw_header(
            cpu=sys_mon.get_cpu(), 
            ram=sys_mon.get_ram(), 
            temp=sys_mon.get_temp(), 
            net_type=get_net_status(sys_mon), 
            battery=get_batt_status(sys_mon)
        )
        window.draw_body(m_actual, MENU_ESTRUCTURA[m_actual])
        window.draw_footer(mensaje="Esperando orden...")
        
        # Enviamos el menú completo usando otro nombre de archivo (menu.bmp)
        screen.push_full_screen(filename="menu.bmp")
        time.sleep(4) # Pausa estricta para evitar colisión de panel táctil

    # 2. DIBUJAR MENÚ INICIAL
    print("Enviando Menú Principal...")
    refresh_screen(menu_actual)
    
    ultimo_minuto = datetime.now().minute
    cmd_file_path = "/dev/shm/piscan_cmd.txt"
    print("Sistema Activo. Sensores Táctiles Iniciados.")
    
    try:
        while True:
            # A. RELOJ INTELIGENTE (Actualiza solo el Header)
            minuto_actual = datetime.now().minute
            if minuto_actual != ultimo_minuto:
                if not os.path.exists(cmd_file_path):
                    window.draw_header(
                        cpu=sys_mon.get_cpu(), 
                        ram=sys_mon.get_ram(), 
                        temp=sys_mon.get_temp(), 
                        net_type=get_net_status(sys_mon), 
                        battery=get_batt_status(sys_mon)
                    )
                    screen.push_header() 
                    time.sleep(0.5) 
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
                                refresh_screen(menu_actual)
                            
                            elif opcion["tipo"] == "accion":
                                # Refresco del Footer para simular que carga
                                window.draw_footer(mensaje=f"Iniciando: {opcion['nombre']}")
                                screen.push_footer()
                                time.sleep(1)
                                
                                # Simulación del trabajo de la herramienta
                                time.sleep(1.0)
                                
                                # Vuelve al estado base
                                window.draw_footer(mensaje="Esperando orden...")
                                screen.push_footer()
                                time.sleep(1)

            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Apagando...")
        screen.clear(color="#000000")
        screen.push_full_screen(filename="apagado.bmp")

if __name__ == "__main__":
    main()