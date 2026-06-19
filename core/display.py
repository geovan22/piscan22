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
        
        # Archivos mágicos que el motor en C está esperando (En la memoria RAM)
        self.img_path = "/dev/shm/piscan_frame.bmp"
        self.flag_path = "/dev/shm/frame_ready"
        
        # 1. Matar cualquier daemon fantasma viejo por seguridad
        subprocess.run(["sudo", "killall", "kedei_daemon"], stderr=subprocess.DEVNULL)
        time.sleep(0.5) # Pausa breve para liberar el bus SPI
        
        # 2. Arrancar el motor en C en segundo plano
        print("[DISPLAY] Iniciando Kedei Daemon en segundo plano...")
        self.daemon = subprocess.Popen(["sudo", self.daemon_path])

    def clear(self, color="black"):
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def push_to_screen(self):
        """Envía el lienzo al Daemon instantáneamente y sin barrido"""
        # 1. Guardar la imagen en RAM
        self.image.save(self.img_path)
        
        # 2. Crear el archivo bandera para despertar al Daemon
        with open(self.flag_path, "w") as f:
            f.write("1")

    def __del__(self):
        # Limpieza al cerrar el programa
        if hasattr(self, 'daemon'):
            self.daemon.kill()
        subprocess.run(["sudo", "killall", "kedei_daemon"], stderr=subprocess.DEVNULL)