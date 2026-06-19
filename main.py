import os
import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from PIL import Image
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def show_splash(screen, espera=5):
    """Carga y muestra el Logo a prueba de fallos visuales"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    splash_path = os.path.join(base_dir, "ui", "assets", "images", "splash.bmp")
    
    try:
        # 1. Forzar limpieza a negro puro
        screen.clear(color="#000000")
        
        # 2. Convert(RGB) arregla cualquier transparencia o formato raro que dejara ver el footer viejo
        splash_img = Image.open(splash_path).convert("RGB").resize((screen.width, screen.height))
        screen.image.paste(splash_img, (0, 0))
        
        # 3. Enviar comando seguro
        screen.push_full_screen() 
        
        if espera > 0:
            time.sleep(espera)
    except OSError:
        print(f"[ERROR] No se encontró la imagen en: {splash_path}")

def main():
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    print("Iniciando PiScan22...")
    show_splash(screen, espera=4)
    
    menu_actual = "Principal"
    opcion_seleccionada = 0
    
    print("Iniciando Interfaz de Monitoreo...")
    
    try:
        while True:
            screen.clear(color="#000000")
            window.draw_header(
                cpu=sys_mon.get_cpu(), 
                ram=sys_mon.get_ram(), 
                temp=sys_mon.get_temp(), 
                connected=sys_mon.is_connected(), 
                battery=sys_mon.get_battery()
            )
            window.draw_body(
                titulo_menu=menu_actual, 
                lista_opciones=MENU_ESTRUCTURA[menu_actual], 
                indice_seleccionado=opcion_seleccionada
            )
            window.draw_footer(mensaje="Sistema Activo y Monitoreando...")
            
            screen.push_to_screen()
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSaliendo de PiScan22... Mostrando logo de despedida.")
        
        # Mandamos pintar el logo pero SIN pausar internamente la función
        show_splash(screen, espera=0)
        
        # CRÍTICO: Le damos 2 segundos exactos de vida a Python para que el
        # motor en C alcance a recibir la orden y pintar la pantalla antes del apagado.
        time.sleep(2)

if __name__ == "__main__":
    main()