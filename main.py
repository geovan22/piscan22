# main.py
import time
from core.config import debug_print
from core.display import ScreenController
from ui.window import MainWindow

def main():
    debug_print("MAIN", "--- INICIANDO PISCAN22 (PRUEBA DE LOGO AISLADA) ---")
    
    screen = ScreenController()
    window = MainWindow(screen)
    
    debug_print("MAIN", "Limpiando pantalla a negro...")
    screen.clear(color="#000000")
    
    window.draw_logo()
    screen.push_full_screen()
    
    debug_print("MAIN", "Logo enviado exitosamente al motor C.")
    debug_print("MAIN", "Entrando en espera infinita. Si la pantalla se pone blanca ahora, el motor C está fallando al leer el BMP.")
    
    try:
        # Nos quedamos aquí para siempre. 
        # La pantalla debería mostrar el logo y NO irse a blanco.
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando sistema por teclado (Ctrl+C)...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()