# core/display.py
import os
import subprocess
import time
from PIL import Image, ImageDraw

class ScreenController:
    def __init__(self):
        self.width = 480
        self.height = 320
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.draw = ImageDraw.Draw(self.image)
        
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.daemon_path = os.path.join(self.base_dir, "core", "kedei_daemon")
        self.cmd_path = "/dev/shm/piscan_cmd.txt"
        
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)
        if os.path.exists("/dev/shm/"):
            subprocess.run("rm -f /dev/shm/*.bmp /dev/shm/piscan_cmd.txt", shell=True)
            
        self.daemon = subprocess.Popen([self.daemon_path])
        time.sleep(2)

    def clear(self, color="black"):
        self.image = Image.new("RGB", (self.width, self.height), color)
        self.draw = ImageDraw.Draw(self.image)

    def push_full_screen(self):
        img_path = "/dev/shm/full.bmp"
        tmp_path = "/dev/shm/full.tmp"
        
        # Guardado atómico
        self.image.convert("RGB").save(tmp_path, format="BMP")
        os.rename(tmp_path, img_path)
        
        # Enviar orden
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 0 {img_path}\n")
            
        # BLOQUEO FÍSICO: Obligamos a Python a no hacer absolutamente NADA 
        # por 1.5 segundos. Esto blinda el bus SPI mientras el C dibuja.
        time.sleep(1.5)

    def __del__(self):
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)