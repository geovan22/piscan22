import os
import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from PIL import Image
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def show_splash(screen):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    splash_path = os.path.join(base_dir, "ui", "assets", "images","splash.bmp")
    try:
        splash_img = Image.open(splash_path).resize((screen.width, screen.height))
        screen.image.paste(splash_img, (0, 0))
        screen.push_to_screen()
        print("Pantalla de inicio cargada. Esperando 5 segundos...")
        time.sleep(5)
    except OSError:
        print("[ERROR] No se encontró splash.bmp")

def main():
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    # 1. Cargar Splash Screen
    show_splash(screen)
    
    # Estado inicial de la UI
    menu_actual = "Principal"
    opcion_seleccionada = 0
    mensaje_footer = "Sistema Listo y Monitoreando..."
    
    print("Dibujando esqueleto base por primera vez...")
    
    # 2. DIBUJAR TODO COMPLETO SOLO UNA VEZ
    screen.clear(color="#000000")
    window.draw_header(cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), connected=sys_mon.is_connected(), battery=sys_mon.get_battery())
    window.draw_body(titulo_menu=menu_actual, lista_opciones=MENU_ESTRUCTURA[menu_actual], indice_seleccionado=opcion_seleccionada)
    window.draw_footer(mensaje=mensaje_footer)
    screen.push_to_screen() # Envío pesado inicial
    
    # Variables de control de memoria (Para saber cuándo dibujar)
    last_header_time = time.time()
    last_menu = menu_actual
    last_opcion = opcion_seleccionada
    last_mensaje = mensaje_footer
    
    print("Entrando a Bucle Asíncrono de Zonas...")
    
    try:
        while True:
            current_time = time.time()
            
            # --- ZONA 1: HEADER (Se actualiza automáticamente cada 2 segundos) ---
            if current_time - last_header_time >= 2.0:
                window.draw_header(cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), connected=sys_mon.is_connected(), battery=sys_mon.get_battery())
                # Enviar SOLO el recorte superior (x1=0, y1=0, x2=480, y2=30)
                screen.push_zone((0, 0, screen.width, 30)) 
                last_header_time = current_time
                
            # --- ZONA 2: BODY (SOLO se actualiza si cambias de menú o bajas la flecha) ---
            if menu_actual != last_menu or opcion_seleccionada != last_opcion:
                window.draw_body(titulo_menu=menu_actual, lista_opciones=MENU_ESTRUCTURA[menu_actual], indice_seleccionado=opcion_seleccionada)
                # Enviar SOLO el recorte central (x1=0, y1=30, x2=480, y2=290)
                screen.push_zone((0, 30, screen.width, screen.height - 30))
                last_menu = menu_actual
                last_opcion = opcion_seleccionada
                
            # --- ZONA 3: FOOTER (SOLO se actualiza si hay una nueva alerta) ---
            if mensaje_footer != last_mensaje:
                window.draw_footer(mensaje=mensaje_footer)
                # Enviar SOLO el recorte inferior (x1=0, y1=290, x2=480, y2=320)
                screen.push_zone((0, screen.height - 30, screen.width, screen.height))
                last_mensaje = mensaje_footer

            # El bucle ahora puede correr rapidísimo para leer botones sin laggear la pantalla
            time.sleep(0.05) 
            
    except KeyboardInterrupt:
        print("\nSaliendo de PiScan22...")
        screen.clear(color="#000000")
        screen.push_to_screen()

if __name__ == "__main__":
    main()