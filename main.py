# main.py - Punto de entrada principal para la aplicación PiScan
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
    
    print("Iniciando Interfaz...")
    menu_actual = "Principal"
    
    # Dibujo Inicial
    screen.clear(color="#000000")
    window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), sys_mon.is_connected(), sys_mon.get_battery())
    window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
    screen.push_full_screen()
    
    # PAUSA CRÍTICA: Esperamos 2 segundos para que veas el logo 
    # y el bus SPI termine de dibujar antes de pasar al menú.
    time.sleep(2)
    
    menu_actual = "Principal"
    
    def refresh_screen(m_actual):
        """Dibuja la interfaz y bloquea Python hasta que el C termine de transmitir"""
        screen.clear(color="#000000")
        window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), sys_mon.is_connected(), sys_mon.get_battery())
        window.draw_body(m_actual, MENU_ESTRUCTURA[m_actual])
        window.draw_footer(mensaje="Esperando orden...")
        screen.push_full_screen()
        
        # PAUSA CRÍTICA: La Pi 1 B necesita aprox 1 segundo para enviar la imagen completa
        # Esto evita que el panel táctil interrumpa la señal de video.
        time.sleep(1)

    # --- 2. DIBUJO DEL MENÚ INICIAL ---
    refresh_screen(menu_actual)
    
    try:
        while True:
            # Solo procesar táctil si el archivo de comando NO existe (bus libre)
            if not os.path.exists(cmd_file_path):
                pos = touch.get_touch()
                if pos:
                    x, y = pos
                    # Área del menú
                    if 90 < y < 280:
                        indice = int((y - 90) // 45)
                        opciones = MENU_ESTRUCTURA[menu_actual]
                        
                        if 0 <= indice < len(opciones):
                            opcion = opciones[indice]
                            if opcion["tipo"] in ["submenu", "volver"]:
                                menu_actual = opcion["destino"]
                                screen.clear(color="#000000")
                                window.draw_header(sys_mon.get_cpu(), sys_mon.get_ram(), sys_mon.get_temp(), sys_mon.is_connected(), sys_mon.get_battery())
                                window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual])
                                screen.push_full_screen()
                                time.sleep(0.5)
            
            time.sleep(0.2) # Pausa mayor para evitar saturación de bus SPI
            
    except KeyboardInterrupt:
        print("Apagando...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()