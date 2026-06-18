import spidev
from PIL import Image, ImageDraw

class ScreenController:
    def __init__(self):
        self.width = 480
        self.height = 320
        # Lienzo maestro en memoria RAM de Python
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.draw = ImageDraw.Draw(self.image)
        
        # ==============================================================
        # INICIALIZACIÓN DE HARDWARE SPI (La clave de la fluidez)
        # ==============================================================
        try:
            self.spi = spidev.SpiDev()
            # Bus 0, Dispositivo 0 (La pantalla de video). El touch usa el 1.
            self.spi.open(0, 0) 
            # Velocidad al máximo soportado para evitar barridos (48 MHz)
            self.spi.max_speed_hz = 48000000 
            self.spi.mode = 0
        except Exception as e:
            print(f"[ALERTA HARDWARE] No se pudo abrir spidev: {e}")

    def clear(self, color="black"):
        """Limpia el lienzo lógico en Python"""
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def push_to_screen(self):
        """Inyecta la matriz completa de 480x320 cruda por el Bus SPI"""
        if not hasattr(self, 'spi'): return
        
        # Convertir la imagen de Pillow al formato nativo 16-bits (RGB565)
        # y pasarlo a un array de bytes que spidev pueda procesar al instante
        raw_bytes = bytearray(self.image.convert("BGR;16").tobytes())
        
        try:
            # writebytes2 es ultra rápido y no colapsa la memoria
            self.spi.writebytes2(raw_bytes)
        except Exception as e:
            print(f"Error inyectando fotograma SPI: {e}")

    def push_zone(self, box):
        """
        ACTUALIZACIÓN PARCIAL: Corta solo la zona que cambió (Ej. Header)
        y la manda por SPI sin reiniciar la pantalla ni borrar lo demás.
        """
        if not hasattr(self, 'spi'): return
        
        # Extraer exactamente el pedacito de pantalla
        zona_img = self.image.crop(box)
        raw_bytes = bytearray(zona_img.convert("BGR;16").tobytes())
        
        try:
            # Enviar únicamente los bytes del recorte
            self.spi.writebytes2(raw_bytes)
        except Exception as e:
            print(f"Error inyectando zona SPI: {e}")