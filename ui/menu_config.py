# ui/menu_config.py

# Códigos Unicode de FontAwesome Solid
# \uf1eb = WiFi | \uf7d9 = Herramientas | \uf293 = Bluetooth | \uf013 = Engranaje
# \uf1e2 = Bomba (Jammer) | \uf519 = Antena (Radio) | \uf2c2 = Tarjeta ID (RFID) | \uf060 = Flecha Izq

MENU_ESTRUCTURA = {
    "Principal": [
        {"nombre": "Conectar Red", "icono": "\uf1eb", "accion": "menu_red"},
        {"nombre": "Herramientas", "icono": "\uf7d9", "accion": "menu_herramientas"},
        {"nombre": "Bluetooth", "icono": "\uf293", "accion": "menu_bluetooth"},
        {"nombre": "Configuración", "icono": "\uf013", "accion": "menu_config"}
    ],
    "Herramientas": [
        {"nombre": "Jammer", "icono": "\uf1e2", "accion": "run_jammer"},
        {"nombre": "Radio RF", "icono": "\uf519", "accion": "run_radio"},
        {"nombre": "Clonador RFID", "icono": "\uf2c2", "accion": "run_rfid"},
        {"nombre": "Volver", "icono": "\uf060", "accion": "volver_principal"}
    ]
}

# Iconos globales del Header
ICONOS_HEADER = {
    "power": "\uf011",       # Símbolo clásico de encendido
    "reset": "\uf2f9",       # Símbolo de recargar/refrescar
    "wifi_on": "\uf1eb",     # Símbolo de WiFi
    "wifi_off": "\uf071"     # Símbolo de alerta (triángulo)
}