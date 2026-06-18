import os
import subprocess
from PIL import Image, ImageDraw

class ScreenController:
    def __init__(self):
        self.width = 480
        self.height = 320
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.draw = ImageDraw.Draw(self.image)
        
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.kedei_path = os.path.join(self.base_dir, "core", "kedei_lcd")

    def clear(self, color="black"):
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def push_full_screen(self):
        """Solo se usa una vez al arrancar el sistema"""
        ruta = "/dev/shm/full.bmp"
        self.image.save(ruta)
        subprocess.run([self.kedei_path, ruta], check=False)

    def push_header(self):
        """Corta un hilito de 480x30 y lo pega arriba (cero barrido)"""
        ruta = "/dev/shm/header.bmp"
        # Coordenadas: (Izquierda, Arriba, Derecha, Abajo)
        zona = self.image.crop((0, 0, 480, 30))
        zona.save(ruta)
        # Se le pasa el archivo y las coordenadas X=0, Y=0
        subprocess.run([self.kedei_path, ruta, "0", "0"], check=False)

    def push_body(self):
        """Actualiza solo el menú central"""
        ruta = "/dev/shm/body.bmp"
        zona = self.image.crop((0, 30, 480, 290))
        zona.save(ruta)
        subprocess.run([self.kedei_path, ruta, "0", "30"], check=False)

    def push_footer(self):
        """Actualiza solo la barra inferior"""
        ruta = "/dev/shm/footer.bmp"
        zona = self.image.crop((0, 290, 480, 320))
        zona.save(ruta)
        subprocess.run([self.kedei_path, ruta, "0", "290"], check=False)