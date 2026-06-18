import os
import subprocess
from PIL import Image, ImageDraw

class ScreenController:
    def __init__(self):
        # Resolución nativa de la pantalla Kedei 3.5"
        self.width = 480
        self.height = 320
        
        # Crear el lienzo en memoria (imagen base)
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.draw = ImageDraw.Draw(self.image)
        
        # Rutas dinámicas seguras
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.kedei_path = os.path.join(self.base_dir, "core", "kedei_lcd")
        
        # OPTIMIZACIÓN: Escribir el BMP temporal directamente en la RAM (/dev/shm)
        # Esto evita el desgaste de la MicroSD y acelera la comunicación con C.
        self.temp_img = "/dev/shm/piscan_temp.bmp"

    def clear(self, color="black"):
        """Limpia la pantalla pintando un rectángulo del tamaño total"""
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def push_to_screen(self):
        """Guarda el lienzo en la RAM y ejecuta el motor en C"""
        # Guardar la imagen generada por Pillow en la memoria RAM
        self.image.save(self.temp_img)
        
        # Llamar al ejecutable en C inyectando la imagen desde la RAM
        try:
            subprocess.run([self.kedei_path, self.temp_img], check=True)
        except Exception as e:
            print(f"Error de comunicación con Kedei LCD: {e}")

    def push_zone(self, box):
        """
        Corta una sección específica de la RAM y la envía al driver C 
        con sus coordenadas para evitar recargar (y parpadear) toda la pantalla.
        box = (x_inicial, y_inicial, x_final, y_final)
        """
        x_offset = box[0]
        y_offset = box[1]
        
        # Cortamos solo la parte de la imagen que cambió
        zona_img = self.image.crop(box)
        zona_img.save(self.temp_img)
        
        try:
            # Enviamos la imagen diminuta y le indicamos al motor en C dónde pegarla
            import subprocess
            subprocess.run([self.kedei_path, self.temp_img, str(x_offset), str(y_offset)], check=True)
        except Exception as e:
            print(f"Error actualizando zona: {e}")