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
        
        self.img_path = "/dev/shm/piscan_frame.bmp"
        self.flag_path = "/dev/shm/frame_ready"
        
        print("[DISPLAY] Limpiando memoria y procesos fantasma...")
        subprocess.run(["sudo", "killall", "kedei_daemon"], stderr=subprocess.DEVNULL)
        
        # CRÍTICO: Borrar archivos viejos de la RAM para que el motor C no crashee al arrancar
        subprocess.run(["sudo", "rm", "-f", self.img_path, self.flag_path])
        time.sleep(0.5)
        
        print("[DISPLAY] Iniciando Kedei Daemon en segundo plano...")
        self.daemon = subprocess.Popen(["sudo", self.daemon_path])
        
        # CRÍTICO: Darle 2 segundos al motor en C para resetear eléctricamente la LCD 
        # y pintarla de negro ANTES de que Python dispare la primera imagen.
        print("[DISPLAY] Despertando el hardware de video...")
        time.sleep(2)

    def clear(self, color="black"):
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def push_to_screen(self):
        try:
            # 1. Guardar forzando explícitamente el formato BMP de 24 bits
            self.image.convert("RGB").save(self.img_path, format="BMP")
            
            # 2. Levantar la bandera para despertar al Daemon
            with open(self.flag_path, "w") as f:
                f.write("1")
        except Exception as e:
            print(f"[ERROR DISPLAY] Falló la inyección en RAM: {e}")

    def __del__(self):
        if hasattr(self, 'daemon'):
            self.daemon.kill()
        subprocess.run(["sudo", "killall", "kedei_daemon"], stderr=subprocess.DEVNULL)