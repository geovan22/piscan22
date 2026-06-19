# ui/menu_config.py

# Códigos Unicode de FontAwesome Solid
ICONOS_HEADER = {
    "power": "\uf011",       # Símbolo clásico de encendido
    "reset": "\uf2f9",       # Símbolo de recargar/refrescar
    "wifi_on": "\uf1eb",     # Símbolo de WiFi
    "wifi_off": "\uf071",    # Símbolo de alerta (triángulo)
    "battery": "\uf240"
}

MENU_ESTRUCTURA = {
    "Principal": [
        {"nombre": "Conectar Red", "icono": "\uf1eb", "tipo": "submenu", "destino": "Red"},
        {"nombre": "Herramientas", "icono": "\uf7d9", "tipo": "submenu", "destino": "Herramientas"},
        {"nombre": "Bluetooth", "icono": "\uf293", "tipo": "submenu", "destino": "Bluetooth"},
        {"nombre": "Configuración", "icono": "\uf013", "tipo": "submenu", "destino": "Configuracion"}
    ],
    "Herramientas": [
        {"nombre": "Jammer", "icono": "\uf1e2", "tipo": "accion", "comando": "run_jammer"},
        {"nombre": "Radio RF", "icono": "\uf519", "tipo": "accion", "comando": "run_radio"},
        {"nombre": "Clonador RFID", "icono": "\uf2c2", "tipo": "accion", "comando": "run_rfid"},
        {"nombre": "Volver", "icono": "\uf060", "tipo": "volver", "destino": "Principal"}
    ],
    "Red": [
        {"nombre": "Escanear Redes", "icono": "\uf1eb", "tipo": "accion", "comando": "scan_wifi"},
        {"nombre": "Volver", "icono": "\uf060", "tipo": "volver", "destino": "Principal"}
    ],
    "Bluetooth": [
        {"nombre": "Escanear BLE", "icono": "\uf293", "tipo": "accion", "comando": "scan_ble"},
        {"nombre": "Volver", "icono": "\uf060", "tipo": "volver", "destino": "Principal"}
    ],
    "Configuracion": [
        {"nombre": "Apagar Sistema", "icono": "\uf011", "tipo": "accion", "comando": "sys_poweroff"},
        {"nombre": "Volver", "icono": "\uf060", "tipo": "volver", "destino": "Principal"}
    ]
}