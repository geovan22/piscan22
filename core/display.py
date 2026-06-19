import os
import subprocess
import time
from PIL import Image

class ScreenController:
    CMD_NAME = "IMG"

    def __init__(self):
        self.width = 480
        self.height = 320
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.daemon_path = os.path.join(self.base_dir, "core", "kedei_daemon")
        self.cmd_path = "/dev/shm/piscan_cmd.txt"
        
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "-f", "/dev/shm/*.bmp", self.cmd_path], shell=True)
        time.sleep(0.5)
        
        self.daemon = subprocess.Popen([self.daemon_path])
        time.sleep(2)

    def clear(self, color="black"):
        self.image = Image.new("RGB", (self.width, self.height), color)

    def _send_cmd(self, img_path, x, y):
        # 1. Asegurar que el buzón esté vacío antes de guardar la nueva imagen
        if os.path.exists(self.cmd_path):
            os.remove(self.cmd_path)
        
        # 2. Guardar imagen y luego enviar comando
        self.image.convert("RGB").save(img_path, format="BMP")
        with open(self.cmd_path, "w") as f:
            f.write(f"{self.CMD_NAME} {x} {y} {img_path}\n")

    def push_full_screen(self):
        self._send_cmd("/dev/shm/full.bmp", 0, 0)

    def push_header(self):
        img_path = "/dev/shm/header.bmp"
        self.image.crop((0, 0, 480, 30)).save(img_path, format="BMP")
        with open(self.cmd_path, "w") as f:
            f.write(f"{self.CMD_NAME} 0 0 {img_path}\n")

    def push_body(self):
        img_path = "/dev/shm/body.bmp"
        self.image.crop((0, 30, 480, 290)).save(img_path, format="BMP")
        with open(self.cmd_path, "w") as f:
            f.write(f"{self.CMD_NAME} 0 30 {img_path}\n")

    def __del__(self):
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)