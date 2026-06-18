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
        # RAM Disk para máxima velocidad
        self.temp_img = "/dev/shm/piscan_temp.bmp" 

    def clear(self, color="black"):
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def push_to_screen(self):
        """Guarda en RAM y ejecuta el motor en C (El estándar para Kedei)"""
        self.image.save(self.temp_img)
        try:
            subprocess.run([self.kedei_path, self.temp_img], check=True)
        except Exception as e:
            print(f"Error de comunicación LCD: {e}")