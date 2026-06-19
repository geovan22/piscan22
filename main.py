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
    debug_print("MAIN", "=== INICIANDO FASE 4.1: UI SECTORIZADA + RELOJ INTELIGENTE ===")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen()
    
    # 1. LOGO DE INICIO AL 100% (Pantalla completa, el bus está fresco)
    debug_print("MAIN", "Mostrando Logo redimensionado...")
    screen.clear(color="#000000")
    window.draw_logo()
    screen.push_full_screen()
    time.sleep(3.5) # Pausa para apreciar el logo y estabilizar el bus
    
    # 2. RENDERIZADO INICIAL SECTORIZADO (Como en la Fase 3 que sí funcionó)
    debug_print("MAIN", "Dibujando UI en la RAM...")
    menu_actual = "Principal"
    
    def refresh_full_ui(menu_name):
        """Dibuja en RAM y envía pieza por pieza para no saturar la pantalla blanca."""
        screen.clear(color="#000000")
        window.draw_header(
            cpu=sys_mon.get_cpu(), 
            ram=sys_mon.get_ram(), 
            temp=sys_mon.get_temp(), 
            net_type=sys_mon.get_network_type(), 
            battery=sys_mon.get_battery()
        )
        window.draw_body(menu_name, MENU_ESTRUCTURA[menu_name])
        window.draw_footer(mensaje="Sistema Activo.")
        
        debug_print("MAIN", f"Enviando sectores: Menú {menu_name}")
        
        # Envíos en bloque pequeño (Cero desfaces, cero pantallas blancas)
        screen.push_header()
        time.sleep(0.5)
        
        screen.push_body()
        time.sleep(0.5)
        
        screen.push_footer()
        time.sleep(0.5)

    # Mandamos el menú inicial por sectores
    refresh_full_ui(menu_actual)
    
    # Variables de control
    ultimo_minuto = datetime.now().minute
    cmd_file_path = "/dev/shm/piscan_cmd.txt"
    
    # 3. BUCLE PRINCIPAL (TÁCTIL + HEADER INDEPENDIENTE)
    debug_print("MAIN", "Entrando a bucle principal (Táctil activado)...")
    
    try:
        while True:
            # A. EVENTO 1: VERIFICAR TÁCTIL (Navegación)
            if not os.path.exists(cmd_file_path):
                pos = touch.get_touch()
                if pos:
                    x, y = pos
                    # Detectar si el toque fue en la zona del menú (Y: 90 a 280)
                    if 90 < y < 280:
                        indice = int((y - 90) // 45)
                        opciones = MENU_ESTRUCTURA[menu_actual]
                        
                        if 0 <= indice < len(opciones):
                            opcion = opciones[indice]
                            
                            if opcion["tipo"] in ["submenu", "volver"]:
                                menu_actual = opcion["destino"]
                                refresh_full_ui(menu_actual)

            # B. EVENTO 2: RELOJ INTELIGENTE (Actualiza Header solo si cambia el minuto)
            minuto_actual = datetime.now().minute
            if minuto_actual != ultimo_minuto:
                debug_print("MAIN", "Cambio de minuto detectado. Actualizando Header...")
                window.draw_header(
                    cpu=sys_mon.get_cpu(), 
                    ram=sys_mon.get_ram(), 
                    temp=sys_mon.get_temp(), 
                    net_type=sys_mon.get_network_type(), 
                    battery=sys_mon.get_battery()
                )
                screen.push_header() 
                ultimo_minuto = minuto_actual
            
            # C. DESCANSO DEL PROCESADOR
            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando sistema por orden del usuario...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()