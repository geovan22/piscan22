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
        time.sleep(0.1) # Breve pausa para asentar el archivo en la RAM
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 0 {img_path}\n")

    def push_header(self):
        img_path = "/dev/shm/header.bmp"
        zona = self.image.crop((0, 0, self.width, 30))
        zona.save(img_path, format="BMP")
        time.sleep(0.05)
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG 0 0 {img_path}\n")

    def __del__(self):
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)