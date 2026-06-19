import os
import subprocess
import time
from PIL import Image, ImageDraw

class ScreenController:
    # =========================================================================
    # CONFIGURACIÓN DEL COMANDO:
    # Si la pantalla se queda en negro con "BMP", cambia esto a "IMG"
    # =========================================================================
    CMD_NAME = "BMP"

    def __init__(self):
        self.width = 480
        self.height = 320
        # Lienzo maestro en la RAM de Python
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.draw = ImageDraw.Draw(self.image)
        
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.daemon_path = os.path.join(self.base_dir, "core", "kedei_daemon")
        
        # El buzón de texto plano donde tu daemon en C espera las órdenes
        self.cmd_path = "/dev/shm/piscan_cmd.txt"
        
        print("[DISPLAY] Limpiando procesos fantasma y buzón antiguo...")
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)
        subprocess.run(["rm", "-f", self.cmd_path, "/dev/shm/*.bmp"], shell=True, stderr=subprocess.DEVNULL)
        time.sleep(0.5)
        
        print("[DISPLAY] Iniciando Motor Gráfico de fondo (Kedei Daemon)...")
        self.daemon = subprocess.Popen([self.daemon_path])
        
        print("[DISPLAY] Esperando sincronización del bus de video...")
        time.sleep(2)

    def clear(self, color="black"):
        """Limpia el lienzo virtual de Python"""
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)

    def push_to_screen(self):
        """Mantiene la compatibilidad con el flujo general enviando pantalla completa"""
        self.push_full_screen()

    def push_full_screen(self):
        """Guarda la imagen completa y le ordena al Daemon mapearla en (0,0)"""
        img_path = "/dev/shm/full.bmp"
        self.image.save(img_path)
        self._send_cmd(f"{self.CMD_NAME} 0 0 {img_path}")

    def push_header(self):
        """Corta la franja del Header (480x30) y la reescribe de forma instantánea"""
        img_path = "/dev/shm/header.bmp"
        zona = self.image.crop((0, 0, 480, 30))
        zona.save(img_path)
        self._send_cmd(f"{self.CMD_NAME} 0 0 {img_path}")

    def push_body(self):
        """Corta el área del menú central y la envía indicando el desplazamiento Y=30"""
        img_path = "/dev/shm/body.bmp"
        zona = self.image.crop((0, 30, 480, 290))
        zona.save(img_path)
        self._send_cmd(f"{self.CMD_NAME} 0 30 {img_path}")

    def push_footer(self):
        """Corta la barra de estado inferior y la inyecta en Y=290"""
        img_path = "/dev/shm/footer.bmp"
        zona = self.image.crop((0, 290, 480, 320))
        zona.save(img_path)
        self._send_cmd(f"{self.CMD_NAME} 0 290 {img_path}")

    def _send_cmd(self, command_str):
        """Escribe la línea exacta en el archivo compartido de la RAM para despertar al C"""
        try:
            with open(self.cmd_path, "w") as f:
                f.write(command_str + "\n")
        except Exception as e:
            print(f"[ERROR DISPLAY] Falló el envío al buzón: {e}")

    def __del__(self):
        """Asegura liberar los recursos del sistema al cerrar la aplicación"""
        if hasattr(self, 'daemon'):
            self.daemon.kill()
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)