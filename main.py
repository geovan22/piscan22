from core.display import ScreenController

def main():
    print("Inicializando Motor Gráfico PiScan22...")
    screen = ScreenController()
    
    # Vamos a pintar la pantalla de un verde neón brillante 
    # para confirmar que tenemos control total de los colores.
    screen.clear(color="#00FF00")
    screen.push_to_screen()
    
    print("¡Lienzo enviado! Revisa tu pantalla LCD Kedei.")

if __name__ == "__main__":
    main()