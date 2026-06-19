import os
import subprocess
import time
from PIL import Image, ImageDraw

class ScreenController:
    CMD_NAME = "IMG"

    def __init__(self):
        self.width = 480
        self.height = 320
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.draw = ImageDraw.Draw(self.image)
        
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.daemon_path = os.path.join(self.base_dir, "core", "kedei_daemon")
        self.cmd_path = "/dev/shm/piscan_cmd.txt"
        
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "-f", self.cmd_path, "/dev/shm/*.bmp"], shell=True, stderr=subprocess.DEVNULL)
        time.sleep(0.5)
        
        self.daemon = subprocess.Popen([self.daemon_path])
        time.sleep(2)

    def clear(self, color="black"):
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def _wait_for_daemon(self):
        """SEMÁFORO: Aumentado a 10 segundos (1000 ciclos) para la Raspberry Pi 1 B"""
        timeout = 0
        while os.path.exists(self.cmd_path) and timeout < 1000:
            time.sleep(0.01)
            timeout += 1

    def push_to_screen(self):
        self.push_full_screen()

    def push_full_screen(self):
        self._wait_for_daemon() # Espera antes de enviar
        img_path = "/dev/shm/full.bmp"
        self.image.save(img_path)
        self._send_cmd(f"{self.CMD_NAME} 0 0 {img_path}")

    def push_header(self):
        self._wait_for_daemon()
        img_path = "/dev/shm/header.bmp"
        zona = self.image.crop((0, 0, 480, 30))
        zona.save(img_path)
        self._send_cmd(f"{self.CMD_NAME} 0 0 {img_path}")

    def push_body(self):
        self._wait_for_daemon()
        img_path = "/dev/shm/body.bmp"
        zona = self.image.crop((0, 30, 480, 290))
        zona.save(img_path)
        self._send_cmd(f"{self.CMD_NAME} 0 30 {img_path}")

    def push_footer(self):
        self._wait_for_daemon()
        img_path = "/dev/shm/footer.bmp"
        zona = self.image.crop((0, 290, 480, 320))
        zona.save(img_path)
        self._send_cmd(f"{self.CMD_NAME} 0 290 {img_path}")

    def _send_cmd(self, command_str):
        try:
            with open(self.cmd_path, "w") as f:
                f.write(command_str + "\n")
        except Exception as e:
            pass

    def __del__(self):
        if hasattr(self, 'daemon'):
            self.daemon.kill()
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)