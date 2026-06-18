import os
import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from PIL import Image
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

def show_splash(screen):
    """Carga y muestra la imagen de inicio (Splash Screen) a pantalla completa"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    splash_path = os.path.join(base_dir, "ui", "assets", "images", "splash.bmp")
    
    try:
        # Imprimimos la ruta para estar 100% seguros
        print(f"Intentando abrir: {splash_path}") 
        
        splash_img = Image.open(splash_path).resize((screen.width, screen.height))
        screen.image.paste(splash_img, (0, 0))
        
        screen.push_full_screen() 
        print("Pantalla de inicio cargada. Esperando 5 segundos...")
        time.sleep(5)
    except Exception as e:
        # AQUI ESTÁ EL TRUCO: Le pedimos a Python que nos diga exactamente qué le molesta
        print(f"\n[ERROR DETALLADO] Falló la imagen: {e}\n")

def main():
    # Inicializar todos los controladores
    screen = ScreenController()
    sys_mon = SystemMonitor()
    window = MainWindow(screen)
    
    # 1. Mostrar Splash Screen
    show_splash(screen)
    
    # Variables de estado iniciales para el menú
    menu_actual = "Principal"
    opcion_seleccionada = 0
    
    print("Pintando estructura base (Solo habrá un barrido inicial de pantalla)...")
    
    # 2. Dibujar todo el esqueleto (Fondo, Cabecera, Cuerpo y Pie) en la RAM
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
    
    # 3. Enviar la imagen COMPLETA por única vez para establecer el menú en la LCD
    screen.push_full_screen()
    
    print("Iniciando reloj en el Header (Actualización por zonas fluidas)...")
    
    # 4. Bucle principal de actualización (Solo actualiza el pedacito de arriba)
    try:
        while True:
            # Re-escribimos los datos frescos SOLO en la cabecera dentro de la RAM
            window.draw_header(
                cpu=sys_mon.get_cpu(), 
                ram=sys_mon.get_ram(), 
                temp=sys_mon.get_temp(), 
                connected=sys_mon.is_connected(), 
                battery=sys_mon.get_battery()
            )
            
            # ¡LA MAGIA! Enviamos únicamente la tira de 30 píxeles superior.
            # El ejecutable C (kedei_lcd_spidev) detectará esto y NO hará barrido.
            screen.push_header()
            
            # Esperamos 2 segundos antes de volver a leer la hora y la RAM
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSaliendo de PiScan22...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()