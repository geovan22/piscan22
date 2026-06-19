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
        
        # Rutas exactas que espera el bucle en C de tu patcher_v3
        self.img_path = "/dev/shm/piscan_frame.bmp"
        self.flag_path = "/dev/shm/frame_ready"
        
        print("[DISPLAY] Limpiando memoria y procesos fantasma...")
        # Eliminamos el "sudo" interno ya que Python ya corre como root
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "-f", self.img_path, self.flag_path])
        time.sleep(0.5)
        
        print("[DISPLAY] Iniciando Kedei Daemon en segundo plano...")
        # Al quitar "sudo", el Daemon arranca de forma directa e instantánea
        self.daemon = subprocess.Popen([self.daemon_path])
        
        print("[DISPLAY] Despertando el hardware de video...")
        time.sleep(2)

    def clear(self, color="black"):
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def push_to_screen(self):
        """Guarda el mapa de bits en RAM y levanta la bandera para el Daemon"""
        try:
            self.image.convert("RGB").save(self.img_path, format="BMP")
            with open(self.flag_path, "w") as f:
                f.write("1")
        except Exception as e:
            print(f"[ERROR DISPLAY] Falló la inyección en RAM: {e}")

    def __del__(self):
        # Asegurar el cierre del proceso al salir
        if hasattr(self, 'daemon'):
            self.daemon.kill()
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)