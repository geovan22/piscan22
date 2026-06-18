import os
from PIL import Image, ImageDraw

class ScreenController:
    def __init__(self):
        self.width = 480
        self.height = 320
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.draw = ImageDraw.Draw(self.image)
        
        # Detectar el Framebuffer nativo de video (Usualmente fb1 para pantallas SPI, o fb0)
        self.fb_path = "/dev/fb1" if os.path.exists("/dev/fb1") else "/dev/fb0"

    def clear(self, color="black"):
        """Limpia el lienzo en la memoria de Python"""
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def push_to_screen(self):
        """Envía TODO el lienzo a la pantalla en bytes puros (Sin imágenes)"""
        try:
            # BGR;16 es el formato interno exacto (RGB565) que usan estas pantallas
            raw_bytes = self.image.convert("BGR;16").tobytes()
            with open(self.fb_path, "wb") as fb:
                fb.write(raw_bytes)
        except Exception as e:
            print(f"Error escribiendo en memoria de video: {e}")

    def push_zone(self, box):
        """ 
        Actualiza SOLO un segmento (ej. Header) inyectando bytes en su offset.
        ¡Cero parpadeos, cero barridos, cero archivos guardados!
        """
        x_offset, y_offset, x_final, y_final = box
        zona_img = self.image.crop(box)
        raw_bytes = zona_img.convert("BGR;16").tobytes()
        
        zona_width = x_final - x_offset
        zona_height = y_final - y_offset
        bytes_por_pixel = 2 # 16 bits = 2 bytes

        try:
            with open(self.fb_path, "rb+") as fb:
                # Si la zona ocupa todo el ancho (como nuestro Header que es de 480px)
                if zona_width == self.width:
                    offset = (y_offset * self.width) * bytes_por_pixel
                    fb.seek(offset)
                    fb.write(raw_bytes)
                else:
                    # Si es un recuadro más pequeño, escribimos fila por fila
                    for y in range(zona_height):
                        start = y * zona_width * bytes_por_pixel
                        end = start + (zona_width * bytes_por_pixel)
                        offset = ((y_offset + y) * self.width + x_offset) * bytes_por_pixel
                        fb.seek(offset)
                        fb.write(raw_bytes[start:end])
        except Exception as e:
            print(f"Error escribiendo zona parcial en memoria: {e}")