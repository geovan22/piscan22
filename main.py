# main.py
"""
PiScan22 - Entry Point
Raspberry Pi B (700MHz / 512MB) + KeDei 3.5" SPI 480x320

Flujo de arranque:
  1. Inicia el daemon y muestra splash.bmp
  2. Dibuja el menú completo inicial
  3. Loop principal:
     - Refresca solo el header cada HEADER_REFRESH_SECS segundos
     - Detecta toque y actualiza body/footer según corresponda
"""

import time
from core.display import ScreenController
from core.system_info import SystemMonitor
from core.touch import TouchScreen
from ui.window import MainWindow
from ui.menu_config import MENU_ESTRUCTURA

# ------------------------------------------------------------------
# Configuración
# ------------------------------------------------------------------

HEADER_REFRESH_SECS = 5   # Cada cuántos segundos se actualiza el header
TOUCH_DEBOUNCE_SECS = 0.4  # Tiempo mínimo entre toques aceptados
LOGO_DISPLAY_SECS   = 3    # Tiempo que se muestra el splash

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def get_stats(sys_mon: SystemMonitor):
    """Obtiene todos los datos del sistema de una vez."""
    return {
        "cpu":      sys_mon.get_cpu(),
        "ram":      sys_mon.get_ram(),
        "temp":     sys_mon.get_temp(),
        "net_type": sys_mon.get_network_type(),   # 'wifi' | 'lan' | 'disconnected'
        "battery":  sys_mon.get_battery(),
    }


def draw_and_push_header(screen, window, sys_mon):
    """Refresca solo el header: dibuja + envía la región."""
    s = get_stats(sys_mon)
    window.draw_header(s["cpu"], s["ram"], s["temp"], s["net_type"], s["battery"])
    screen.push_header()


def draw_and_push_footer(screen, window, mensaje):
    """Refresca solo el footer: dibuja + envía la región."""
    window.draw_footer(mensaje)
    screen.push_footer()


def draw_and_push_body(screen, window, menu_actual, indice=0):
    """Refresca solo el body: dibuja + envía la región."""
    window.draw_body(menu_actual, MENU_ESTRUCTURA[menu_actual], indice)
    screen.push_body()


def draw_full_ui(screen, window, sys_mon, menu_actual, mensaje="Listo."):
    """Dibuja y envía los 3 componentes de una sola vez."""
    s = get_stats(sys_mon)
    window.draw_all(
        titulo_menu=menu_actual,
        lista_opciones=MENU_ESTRUCTURA[menu_actual],
        cpu=s["cpu"], ram=s["ram"], temp=s["temp"],
        net_type=s["net_type"], battery=s["battery"],
        mensaje=mensaje
    )
    screen.push_full_screen()


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():
    print("=== PISCAN22 INICIANDO ===")

    # Inicializar subsistemas
    screen  = ScreenController()   # Arranca el daemon, pantalla negra
    sys_mon = SystemMonitor()
    window  = MainWindow(screen)
    touch   = TouchScreen()

    # 1. SPLASH
    print("[BOOT] Mostrando splash...")
    window.draw_logo()
    screen.push_full_screen()
    time.sleep(LOGO_DISPLAY_SECS)

    # 2. UI INICIAL
    menu_actual = "Principal"
    print(f"[BOOT] Dibujando menú: {menu_actual}")
    draw_full_ui(screen, window, sys_mon, menu_actual, "Sistema listo.")

    # Timestamps para control de refresco
    last_header_time = time.time()
    last_touch_time  = 0.0

    print("[MAIN] Loop principal activo.")

    # 3. LOOP PRINCIPAL
    try:
        while True:
            now = time.time()

            # --- Refresco periódico del header ---
            if now - last_header_time >= HEADER_REFRESH_SECS:
                draw_and_push_header(screen, window, sys_mon)
                last_header_time = now

            # --- Lectura de toque con debounce ---
            pos = touch.get_touch()
            if pos and (now - last_touch_time) >= TOUCH_DEBOUNCE_SECS:
                last_touch_time = now
                x, y = pos

                # El body empieza en y=32 y termina en y=290
                # Cada ítem ocupa 44px, con el primer ítem en y=32+50=82
                BODY_Y_START = 32 + 50   # = 82
                ITEM_HEIGHT  = 44

                if BODY_Y_START <= y < 290:
                    indice  = int((y - BODY_Y_START) // ITEM_HEIGHT)
                    opciones = MENU_ESTRUCTURA[menu_actual]

                    if 0 <= indice < len(opciones):
                        opcion = opciones[indice]
                        tipo   = opcion.get("tipo")

                        print(f"[TOUCH] Opción {indice}: {opcion['nombre']} (tipo={tipo})")

                        if tipo in ("submenu", "volver"):
                            # Cambiar de menú: actualizar body y footer
                            menu_actual = opcion["destino"]
                            draw_and_push_body(screen, window, menu_actual)
                            draw_and_push_footer(screen, window, f"Menú: {menu_actual}")

                        elif tipo == "accion":
                            # Mostrar en footer que se ejecuta la acción
                            draw_and_push_footer(screen, window,
                                                 f"Ejecutando: {opcion['nombre']}...")
                            
                            # === AQUÍ va la lógica real del comando ===
                            _ejecutar_comando(opcion["comando"])
                            # ==========================================

                            draw_and_push_footer(screen, window, "Listo.")

                        # Toque en header (botones de power/reset)
                elif y < 32:
                    if x < 25:   # Zona del icono power
                        print("[ACTION] Apagando sistema...")
                        draw_and_push_footer(screen, window, "Apagando...")
                        time.sleep(1)
                        import subprocess
                        subprocess.run(["sudo", "poweroff"])
                    elif x < 50:  # Zona del icono reset
                        print("[ACTION] Reiniciando sistema...")
                        draw_and_push_footer(screen, window, "Reiniciando...")
                        time.sleep(1)
                        import subprocess
                        subprocess.run(["sudo", "reboot"])

            time.sleep(0.08)   # ~12 FPS de polling táctil

    except KeyboardInterrupt:
        print("\n[MAIN] Detenido por usuario.")
        screen.clear("black")
        screen.push_full_screen()
        time.sleep(1)


def _ejecutar_comando(comando: str):
    """
    Despachador de comandos. 
    Añade aquí la lógica real de cada herramienta.
    """
    import subprocess

    acciones = {
        "scan_wifi":   lambda: subprocess.Popen(["python3", "tools/wifi_scan.py"]),
        "scan_ble":    lambda: subprocess.Popen(["python3", "tools/ble_scan.py"]),
        "run_jammer":  lambda: subprocess.Popen(["python3", "tools/jammer.py"]),
        "run_radio":   lambda: subprocess.Popen(["python3", "tools/radio_rf.py"]),
        "run_rfid":    lambda: subprocess.Popen(["python3", "tools/rfid_clone.py"]),
        "sys_poweroff":lambda: subprocess.run(["sudo", "poweroff"]),
    }

    accion = acciones.get(comando)
    if accion:
        print(f"[CMD] Lanzando: {comando}")
        accion()
    else:
        print(f"[CMD] Comando desconocido: {comando}")


if __name__ == "__main__":
    main()