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

    def push_logo(self):
        """Usa un archivo exclusivo para el logo"""
        img_path = "/dev/shm/logo.bmp"
        self.image.save(img_path, format="BMP")
        time.sleep(0.1)
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 0 {img_path}\n")

    def push_menu_completo(self):
        """Usa un archivo exclusivo para el menú. Evita corrupción."""
        img_path = "/dev/shm/menu.bmp"
        self.image.save(img_path, format="BMP")
        time.sleep(0.1)
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 0 {img_path}\n")

    def push_header(self):
        """Actualización parcial solo para el reloj"""
        img_path = "/dev/shm/header.bmp"
        zona = self.image.crop((0, 0, self.width, 30))
        zona.save(img_path, format="BMP")
        time.sleep(0.1)
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 0 {img_path}\n")

    def push_footer(self):
        """Actualización parcial solo para mostrar acciones"""
        img_path = "/dev/shm/footer.bmp"
        zona = self.image.crop((0, 290, self.width, 320))
        zona.save(img_path, format="BMP")
        time.sleep(0.1)
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 290 {img_path}\n")

    def __del__(self):
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)