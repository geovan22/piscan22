import os
import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from core.touch import TouchScreen
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def main():
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    touch = TouchScreen()
    touch.init() 
    
    print("Iniciando PiScan22...")
    menu_actual = "Principal"
    
    # 1. Dibujo inicial completo
    screen.clear(color="#000000")
    window.draw_header(cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), connected=sys_mon.is_connected(), battery=sys_mon.get_battery())
    window.draw_body(titulo_menu=menu_actual, lista_opciones=MENU_ESTRUCTURA[menu_actual])
    window.draw_footer(mensaje="Sistema Activo y Monitoreando...")
    screen.push_full_screen()
    
    if hasattr(screen, '_wait_for_daemon'):
        screen._wait_for_daemon()

    last_header_time = time.time()
    
    print("Iniciando Bucle Táctil...")
    try:
        while True:
            current_time = time.time()
            
            # --- TAREA 1: ACTUALIZAR RELOJ (Cada 2 segundos) ---
            if current_time - last_header_time >= 2.0:
                window.draw_header(cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), connected=sys_mon.is_connected(), battery=sys_mon.get_battery())
                screen.push_header()
                last_header_time = current_time
            
            # --- TAREA 2: LEER PANEL TÁCTIL ---
            pos = touch.get_touch()
            if pos is not None:
                x, y = pos
                
                # Evaluar si el toque fue en la zona del menú (Body)
                if 30 < y < 290:
                    indice = int((y - 90) // 45)
                    opciones_actuales = MENU_ESTRUCTURA[menu_actual]
                    
                    if 0 <= indice < len(opciones_actuales):
                        opcion = opciones_actuales[indice]
                        
                        # LOGICA DE NAVEGACIÓN ENTRE NIVELES
                        if opcion["tipo"] in ["submenu", "volver"]:
                            menu_actual = opcion["destino"]
                            # Limpiar memoria RAM de Python y redibujar nuevo menú
                            screen.clear(color="#000000")
                            window.draw_header(cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), connected=sys_mon.is_connected(), battery=sys_mon.get_battery())
                            window.draw_body(titulo_menu=menu_actual, lista_opciones=MENU_ESTRUCTURA[menu_actual])
                            window.draw_footer(mensaje="Navegando...")
                            # Inyectar el menú completo al motor C de golpe
                            screen.push_full_screen()
                            
                        # LOGICA DE EJECUCIÓN DIRECTA
                        elif opcion["tipo"] == "accion":
                            nombre_accion = opcion["nombre"]
                            comando = opcion["comando"]
                            window.draw_footer(mensaje=f"Ejecutando: {nombre_accion}...")
                            screen.push_footer()
                            print(f"[ACCIÓN DISPARADA]: {comando}")
                
                # Pausa anti-rebote (evita doble pulsación por accidente)
                time.sleep(0.4)
            
            # Bucle rápido para mantener la sensibilidad
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\nApagando PiScan22...")
        # APAGADO FRÍO PROFESIONAL A NEGRO
        screen.clear(color="#000000")
        screen.push_full_screen()
        if hasattr(screen, '_wait_for_daemon'):
            screen._wait_for_daemon()
        time.sleep(0.5)

if __name__ == "__main__":
    main()