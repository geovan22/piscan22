import os
from core.display import ScreenController
from PIL import Image

def main():
    print("Cargando Pantalla de Inicio de PiScan_22 OS...")
    screen = ScreenController()
    
    # Obtener la ruta absoluta hacia la imagen splash.bpm
    base_dir = os.path.dirname(os.path.abspath(__file__))
    splash_path = os.path.join(base_dir, "ui", "assets/images", "splash.bmp")
    
    try:
        # 1. Abrir la imagen cargada
        splash_img = Image.open(splash_path)
        
        # 2. Asegurar que tenga el tamaño nativo de la LCD (480x320)
        splash_img = splash_img.resize((screen.width, screen.height))
        
        # 3. Pegar la imagen directamente sobre el lienzo del controlador
        screen.image.paste(splash_img, (0, 0))
        
        print("Imagen splash copiada con éxito al lienzo en memoria.")
        
    except OSError:
        print(f"\n[ERROR] No se pudo encontrar la imagen en: {splash_path}")
        print("Por favor, asegúrate de haber guardado la imagen como 'splash.png' dentro de 'ui/assets/'.\n")
        return

    # 4. Empujar el lienzo optimizado en RAM hacia el ejecutable en C
    screen.push_to_screen()
    
    print("¡Lienzo enviado! Verifica tu pantalla LCD Kedei.")

if __name__ == "__main__":
    main()