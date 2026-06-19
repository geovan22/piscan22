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
        
        # El buzón de comandos que tu motor C está vigilando
        self.cmd_path = "/dev/shm/piscan_cmd.txt"
        
        print("[DISPLAY] Limpiando memoria y buzón de comandos...")
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "-f", self.cmd_path, "/dev/shm/*.bmp"], shell=True, stderr=subprocess.DEVNULL)
        time.sleep(0.5)
        
        print("[DISPLAY] Iniciando Motor Gráfico (Kedei Daemon)...")
        self.daemon = subprocess.Popen([self.daemon_path])
        
        print("[DISPLAY] Despertando hardware de video...")
        time.sleep(2)

    def clear(self, color="black"):
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def push_to_screen(self):
        """Compatibilidad: Envía la pantalla completa (Equivalente a push_full_screen)"""
        self.push_full_screen()

    def push_full_screen(self):
        """Crea el mapa de bits completo y le dice al C que lo dibuje en 0, 0"""
        img_path = "/dev/shm/full.bmp"
        self.image.save(img_path)
        self._send_cmd(f"BMP 0 0 {img_path}")

    def push_header(self):
        """Corta solo el header (30px) y le dice al C que lo pegue en 0, 0"""
        img_path = "/dev/shm/header.bmp"
        zona = self.image.crop((0, 0, 480, 30))
        zona.save(img_path)
        self._send_cmd(f"BMP 0 0 {img_path}")

    def push_body(self):
        """Ejemplo para el futuro: Corta el centro y lo pega en Y=30"""
        img_path = "/dev/shm/body.bmp"
        zona = self.image.crop((0, 30, 480, 290))
        zona.save(img_path)
        self._send_cmd(f"BMP 0 30 {img_path}")

    def _send_cmd(self, command_str):
        """Inyecta el comando mágico en el archivo txt para que el C lo lea y lo borre"""
        try:
            with open(self.cmd_path, "w") as f:
                f.write(command_str + "\n")
        except Exception as e:
            print(f"[ERROR DISPLAY] No se pudo enviar comando: {e}")

    def __del__(self):
        # Apagado seguro del demonio al cerrar PiScan
        if hasattr(self, 'daemon'):
            self.daemon.kill()
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)