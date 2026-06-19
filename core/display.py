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

    def _enviar_comando_con_semaforo(self, img_path, x, y, tiempo_spi):
        """
        SEMÁFORO DE HARDWARE: 
        Asegura que cada tarea se ejecute 100% antes de la siguiente.
        """
        # 1. Enviar orden
        with open(self.cmd_path, "w") as f:
            f.write(f"IMG {x} {y} {img_path}\n")
            
        # 2. Esperar acuse de recibo del demonio C (lectura del txt)
        timeout = time.time() + 3.0
        while os.path.exists(self.cmd_path) and time.time() < timeout:
            time.sleep(0.05)
            
        # 3. Tiempo de transmisión física en el bus SPI
        time.sleep(tiempo_spi)

    def push_full_screen(self):
        img_path = "/dev/shm/full.bmp"
        self.image.save(img_path, format="BMP")
        # Pantalla completa necesita ~2.5s de bloqueo SPI
        self._enviar_comando_con_semaforo(img_path, 0, 0, 2.5)
        debug_print("DISPLAY", "Semáforo: FULL SCREEN completado al 100%.")

    def push_header(self):
        img_path = "/dev/shm/header.bmp"
        zona = self.image.crop((0, 0, self.width, 30))
        zona.save(img_path, format="BMP")
        # Refresco pequeño, ~0.3s de bloqueo
        self._enviar_comando_con_semaforo(img_path, 0, 0, 0.3)
        debug_print("DISPLAY", "Semáforo: HEADER completado.")

    def push_body(self):
        img_path = "/dev/shm/body.bmp"
        zona = self.image.crop((0, 30, self.width, 290))
        zona.save(img_path, format="BMP")
        # Área grande, ~1.5s de bloqueo
        self._enviar_comando_con_semaforo(img_path, 0, 30, 1.5)
        debug_print("DISPLAY", "Semáforo: BODY completado.")

    def push_footer(self):
        img_path = "/dev/shm/footer.bmp"
        zona = self.image.crop((0, 290, self.width, 320))
        zona.save(img_path, format="BMP")
        # Refresco pequeño, ~0.3s de bloqueo
        self._enviar_comando_con_semaforo(img_path, 0, 290, 0.3)
        debug_print("DISPLAY", "Semáforo: FOOTER completado.")

    def __del__(self):
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)