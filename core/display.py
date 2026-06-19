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
        
        debug_print("DISPLAY", "Limpiando RAM y demonio...")
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
        self.image.save(img_path, format="BMP")
        time.sleep(0.1)
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 0 {img_path}\n")

    def push_header(self):
        """Recorta y envía la zona superior (Y: 0 a 30)"""
        img_path = "/dev/shm/header.bmp"
        zona = self.image.crop((0, 0, self.width, 30))
        zona.save(img_path, format="BMP")
        time.sleep(0.05)
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 0 {img_path}\n")
        debug_print("DISPLAY", "Refresco parcial: HEADER enviado.")

    def push_body(self):
        """Recorta y envía el área del menú central (Y: 30 a 290)"""
        img_path = "/dev/shm/body.bmp"
        zona = self.image.crop((0, 30, self.width, 290))
        zona.save(img_path, format="BMP")
        time.sleep(0.05)
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 30 {img_path}\n")
        debug_print("DISPLAY", "Refresco parcial: BODY enviado.")

    def push_footer(self):
        """Recorta y envía la zona de estado inferior (Y: 290 a 320)"""
        img_path = "/dev/shm/footer.bmp"
        zona = self.image.crop((0, 290, self.width, 320))
        zona.save(img_path, format="BMP")
        time.sleep(0.05)
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 290 {img_path}\n")
        debug_print("DISPLAY", "Refresco parcial: FOOTER enviado.")

    def __del__(self):
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)