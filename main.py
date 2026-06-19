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
    debug_print("MAIN", "=== INICIANDO PISCAN22: VERSIÓN ESTABLE ===")
    
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen()
    
    # 1. LOGO DE INICIO
    debug_print("MAIN", "Mostrando Logo redimensionado...")
    screen.clear(color="#000000")
    window.draw_logo()
    screen.push_full_screen()
    # PAUSA SEGURA: El bus SPI descansa mientras miras el logo
    time.sleep(3.5) 
    
    # 2. RENDERIZADO DEL MENÚ (Un solo bloque, con protección de tiempo)
    menu_actual = "Principal"
    
    def refresh_full_ui(menu_name):
        """Dibuja en RAM y manda toda la pantalla, protegiendo el bus."""
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
        window.draw_footer(mensaje="Sistema Activo.")
        
        screen.push_full_screen()
        # ¡EL SECRETO DEL ÉXITO DE LA FASE 2!
        # Bloquea Python 1.5 segundos para que la Raspberry Pi 1 termine
        # de transmitir el video antes de que el táctil interrumpa el bus.
        time.sleep(1.5) 

    # Pintamos el menú por primera vez
    refresh_full_ui(menu_actual)
    
    ultimo_minuto = datetime.now().minute
    
    debug_print("MAIN", "Bucle principal iniciado (Táctil y Reloj Inteligente activos).")
    
    try:
        while True:
            # A. RELOJ INTELIGENTE (Solo actualiza el Header si cambia el minuto)
            minuto_actual = datetime.now().minute
            if minuto_actual != ultimo_minuto:
                debug_print("MAIN", "Minuto cambiado. Actualizando Header...")
                window.draw_header(
                    cpu=sys_mon.get_cpu(), 
                    ram=sys_mon.get_ram(), 
                    temp=sys_mon.get_temp(), 
                    net_type=sys_mon.get_network_type(), 
                    battery=sys_mon.get_battery()
                )
                screen.push_header() 
                time.sleep(0.5) # Pausa de protección del bus SPI para este recorte
                ultimo_minuto = minuto_actual

            # B. PANTALLA TÁCTIL (Navegación)
            pos = touch.get_touch()
            if pos:
                x, y = pos
                # Comprobar si tocó la zona de opciones (Y entre 90 y 280)
                if 90 < y < 280:
                    indice = int((y - 90) // 45)
                    opciones = MENU_ESTRUCTURA[menu_actual]
                    
                    if 0 <= indice < len(opciones):
                        opcion = opciones[indice]
                        
                        if opcion["tipo"] in ["submenu", "volver"]:
                            menu_actual = opcion["destino"]
                            refresh_full_ui(menu_actual)

            # C. PAUSA DE CPU
            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando sistema por orden del usuario...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()