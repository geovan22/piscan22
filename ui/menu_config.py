# ui/menu_config.py

# Usaremos códigos Unicode de FontAwesome para los iconos (ej: "\uf1eb" es WiFi)
MENU_ESTRUCTURA = {
    "Principal": [
        {"nombre": "Conectar Red", "icono": "W", "accion": "menu_red"},
        {"nombre": "Herramientas", "icono": "T", "accion": "menu_herramientas"},
        {"nombre": "Bluetooth", "icono": "B", "accion": "menu_bluetooth"},
        {"nombre": "Configuración", "icono": "C", "accion": "menu_config"}
    ],
    "Herramientas": [
        {"nombre": "Jammer", "icono": "J", "accion": "run_jammer"},
        {"nombre": "Radio RF", "icono": "R", "accion": "run_radio"},
        {"nombre": "Clonador RFID", "icono": "I", "accion": "run_rfid"},
        {"nombre": "<- Volver", "icono": "<", "accion": "volver_principal"}
    ]
}