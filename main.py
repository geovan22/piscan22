# main.py
import time
from core.config import debug_print
from core.display import ScreenController
from ui.window import MainWindow

def main():
    debug_print("MAIN", "=== INICIANDO FASE 1: PRUEBA DE LOGO AISLADA ===")
    
    screen = ScreenController()
    window = MainWindow(screen)
    
    debug_print("MAIN", "Limpiando pantalla a negro...")
    screen.clear(color="#000000")
    
    # 1. Pega la imagen
    window.draw_logo()
    
    # 2. La manda a la pantalla
    screen.push_full_screen()
    
    debug_print("MAIN", "Secuencia de logo completada.")
    debug_print("MAIN", "Entrando en espera infinita. Revisa tu pantalla física.")
    
    try:
        # Bucle de bloqueo. No hace nada más que mantener el script vivo.
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        debug_print("MAIN", "Apagando (Ctrl+C detectado)...")
        screen.clear(color="#000000")
        screen.push_full_screen()

if __name__ == "__main__":
    main()