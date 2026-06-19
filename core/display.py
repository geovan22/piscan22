# core/display.py
import os
import subprocess
import time
from PIL import Image, ImageDraw
from core.config import debug_print

class ScreenController:
    def __init__(self):
        self.width = 480
        self.height = 320
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.draw = ImageDraw.Draw(self.image)
        
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.daemon_path = os.path.join(self.base_dir, "core", "kedei_daemon")
        self.cmd_path = "/dev/shm/piscan_cmd.txt"
        
        debug_print("DISPLAY", "Limpiando demonio anterior y memoria /dev/shm...")
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)
        if os.path.exists("/dev/shm/"):
            subprocess.run("rm -f /dev/shm/*.bmp /dev/shm/piscan_cmd.txt", shell=True)
            
        debug_print("DISPLAY", "Arrancando motor C (kedei_daemon)...")
        self.daemon = subprocess.Popen([self.daemon_path])
        time.sleep(2)
        debug_print("DISPLAY", "Motor C en ejecución.")

    def clear(self, color="black"):
        self.image = Image.new("RGB", (self.width, self.height), color)
        self.draw = ImageDraw.Draw(self.image)

    def push_full_screen(self):
        img_path = "/dev/shm/full.bmp"
        
        debug_print("DISPLAY", f"Guardando imagen en RAM: {img_path}")
        self.image.save(img_path, format="BMP")
        time.sleep(0.1) # Breve pausa para asentar el archivo
        
        debug_print("DISPLAY", "Enviando comando al bus SPI...")
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 0 {img_path}\n")
        debug_print("DISPLAY", "Comando de dibujo enviado.")

    def __del__(self):
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)