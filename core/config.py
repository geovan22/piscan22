# core/config.py

# Cambia a False cuando todo el hardware funcione perfecto
DEBUG_MODE = True

def debug_print(modulo, mensaje):
    """Imprime mensajes en consola solo si el modo debug está activo"""
    if DEBUG_MODE:
        print(f"[DEBUG][{modulo}] {mensaje}")