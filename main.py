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
    print("Iniciando Interfaz Original...")
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    touch = TouchScreen() 
    
    # --- 1. PANTALLA DE LOGO ---
    window.draw_logo()
    screen.push_full_screen()
    # ESCUDO DE TIEMPO: El logo se pintará sin interrupciones táctiles.
    time.sleep(3.5) 
    
    menu_actual = "Principal"
    
    def refresh_screen(m_actual):
        """Tu función original: dibuja, manda y PROTEGE."""
        screen.clear(color="#000000")
        window.draw_header(
            cpu=sys_mon.get_cpu(), 
            ram=sys_mon.get_ram(), 
            temp=sys_mon.get_temp(), 
            connected=sys_mon.is_connected(), 
            battery=sys_mon.get_battery()
        )
        window.draw_body(m_actual, MENU_ESTRUCTURA[m_actual])
        window.draw_footer(mensaje="Esperando orden...")
        screen.push_full_screen()
        
        # ESCUDO DE TIEMPO: Evita el error "se va a blanco al cargar el footer"
        time.sleep(3.5)

    # --- 2. DIBUJAR MENÚ INICIAL ---
    print("Enviando Menú...")
    refresh_screen(menu_actual)
    
    ultimo_minuto = datetime.now().minute
    print("Sistema Activo. Bucle Táctil Iniciado.")
    
    try:
        while True:
            # 3. RELOJ INTELIGENTE (Actualiza solo el header)
            minuto_actual = datetime.now().minute
            if minuto_actual != ultimo_minuto:
                window.draw_header(
                    cpu=sys_mon.get_cpu(), 
                    ram=sys_mon.get_ram(), 
                    temp=sys_mon.get_temp(), 
                    connected=sys_mon.is_connected(), 
                    battery=sys_mon.get_battery()
                )
                screen.push_header() 
                time.sleep(0.5) # Escudo pequeño para el header
                ultimo_minuto = minuto_actual

            # 4. LECTURA TÁCTIL (Tu lógica original intacta)
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
                            # Refresco temporal para indicar carga
                            screen.clear(color="#000000")
                            window.draw_header(
                                cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), 
                                connected=sys_mon.is_connected(), battery=sys_mon.get_battery()
                            )
                            window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
                            window.draw_footer(mensaje=f"Ejecutando: {opcion['nombre']}")
                            screen.push_full_screen()
                            time.sleep(3.5)
                            
                            # (Aquí ejecutarías tu herramienta real)
                            time.sleep(1)
                            
                            # Vuelve a su estado original
                            refresh_screen(menu_actual)

            # Relajar procesador
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Apagando...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()