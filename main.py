import os
import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from PIL import Image
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def show_splash(screen, espera=5):
    """Carga y muestra el Logo protegiendo el renderizado completo"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    splash_path = os.path.join(base_dir, "ui", "assets", "images", "splash.bmp")
    
    try:
        screen.clear(color="#000000")
        splash_img = Image.open(splash_path).convert("RGB").resize((screen.width, screen.height))
        screen.image.paste(splash_img, (0, 0))
        
        # Enviar orden de pintado
        screen.push_full_screen() 
        
        # MAGIA: Obligar a Python a detenerse hasta que el C termine de pintar.
        # Esto soluciona que la pantalla se quede a "3 cuartos".
        if hasattr(screen, '_wait_for_daemon'):
            screen._wait_for_daemon()
            
        if espera > 0:
            time.sleep(espera)
    except OSError:
        print(f"[ERROR] No se encontró la imagen en: {splash_path}")

def main():
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    print("Iniciando PiScan22...")
    show_splash(screen, espera=3)
    
    menu_actual = "Principal"
    opcion_seleccionada = 0
    
    print("Iniciando Interfaz de Monitoreo...")
    
    # 1. Pintamos TODO el menú base una sola vez
    screen.clear(color="#000000")
    window.draw_header(cpu=sys_mon.get_cpu(), ram=sys_mon.get_ram(), temp=sys_mon.get_temp(), connected=sys_mon.is_connected(), battery=sys_mon.get_battery())
    window.draw_body(titulo_menu=menu_actual, lista_opciones=MENU_ESTRUCTURA[menu_actual], indice_seleccionado=opcion_seleccionada)
    window.draw_footer(mensaje="Sistema Activo y Monitoreando...")
    screen.push_full_screen()
    
    if hasattr(screen, '_wait_for_daemon'):
        screen._wait_for_daemon()
    
    try:
        while True:
            # 2. En el bucle, solo reescribimos el Header.
            # Como son solo 30 píxeles, la Pi 1 B lo inyectará al instante y sin barrido visual.
            window.draw_header(
                cpu=sys_mon.get_cpu(), 
                ram=sys_mon.get_ram(), 
                temp=sys_mon.get_temp(), 
                connected=sys_mon.is_connected(), 
                battery=sys_mon.get_battery()
            )
            
            screen.push_header()
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSaliendo de PiScan22... Mostrando logo de despedida.")
        
        # Al llamar esto, el script se quedará bloqueado hasta que el logo se haya dibujado.
        show_splash(screen, espera=0)
        
        # Le damos 1 segundo de gracia al hardware antes de asesinar los procesos.
        time.sleep(1)

if __name__ == "__main__":
    main()