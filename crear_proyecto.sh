#!/bin/bash

echo "Creando estructura base de PiScan22..."

# Crear carpetas principales
mkdir -p core modules security ui/views ui/assets/fonts

# Crear archivos en la raíz
touch README.md main.py

# Crear archivos del Core
touch core/__init__.py core/database.py core/display.py core/touch.py

# Crear archivos de UI
touch ui/__init__.py ui/themes.py

# Crear inits para el resto de módulos
touch modules/__init__.py
touch security/__init__.py

# Añadir un título inicial al README
echo "# PiScan22 - Bitácora de Desarrollo" > README.md

echo "¡Estructura creada con éxito!"
