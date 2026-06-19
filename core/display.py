# core/display.py
import os
import subprocess
import time
from PIL import Image, ImageDraw

class ScreenController:
    """
    Controlador de pantalla KeDei SPI via kedei_daemon.
    
    El daemon lee comandos de /dev/shm/piscan_cmd.txt.
    La sincronización correcta es:
      1. Guardar el BMP en /dev/shm/
      2. Esperar a que el archivo esté completamente escrito (os.fsync)
      3. Escribir el comando al daemon
      4. Esperar la confirmación o un tiempo mínimo seguro
    """

    # Regiones fijas de la pantalla
    REGION_HEADER = (0, 0, 480, 32)   # y: 0-31
    REGION_BODY   = (0, 32, 480, 290) # y: 32-289
    REGION_FOOTER = (0, 290, 480, 320) # y: 290-319

    def __init__(self):
        self.width  = 480
        self.height = 320

        # Canvas principal en memoria (siempre refleja lo que está en pantalla)
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.draw  = ImageDraw.Draw(self.image)

        self.base_dir   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.daemon_path = os.path.join(self.base_dir, "core", "kedei_daemon")
        self.cmd_path   = "/dev/shm/piscan_cmd.txt"
        self.bmp_full   = "/dev/shm/piscan_full.bmp"
        self.bmp_region = "/dev/shm/piscan_region.bmp"

        self._start_daemon()

    # ------------------------------------------------------------------
    # Arranque / parada del daemon
    # ------------------------------------------------------------------

    def _start_daemon(self):
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)
        time.sleep(0.3)

        if os.path.exists("/dev/shm/"):
            subprocess.run("rm -f /dev/shm/piscan_*.bmp /dev/shm/piscan_cmd.txt",
                           shell=True, stderr=subprocess.DEVNULL)

        self.daemon = subprocess.Popen(
            [self.daemon_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # Dar tiempo al daemon para inicializar y mostrar su pantalla negra
        time.sleep(2)

    def __del__(self):
        subprocess.run(["killall", "kedei_daemon"], stderr=subprocess.DEVNULL)

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _save_bmp_sync(self, img, path):
        """Guarda un BMP y hace fsync para garantizar escritura completa antes
        de que el daemon lo lea."""
        img.save(path, format="BMP")
        # fsync: fuerza al kernel a vaciar el buffer al disco/tmpfs
        with open(path, "rb") as f:
            os.fsync(f.fileno())

    def _send_cmd(self, cmd: str, post_delay: float = 0.05):
        """Escribe un comando al daemon y espera post_delay segundos."""
        with open(self.cmd_path, "w") as f:
            f.write(cmd + "\n")
        time.sleep(post_delay)

    # ------------------------------------------------------------------
    # API pública: dibujar sobre canvas interno
    # ------------------------------------------------------------------

    def clear_region(self, region, color="black"):
        """Borra una región del canvas interno. region = (x0,y0,x1,y1)"""
        x0, y0, x1, y1 = region
        self.draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=color)

    def clear(self, color="black"):
        """Borra todo el canvas interno."""
        self.image = Image.new("RGB", (self.width, self.height), color)
        self.draw  = ImageDraw.Draw(self.image)

    # ------------------------------------------------------------------
    # API pública: enviar a la pantalla física
    # ------------------------------------------------------------------

    def push_full_screen(self):
        """Envía el canvas completo a la pantalla."""
        self._save_bmp_sync(self.image, self.bmp_full)
        self._send_cmd(f"IMG 0 0 {self.bmp_full}", post_delay=0.1)

    def push_region(self, region):
        """
        Envía solo una región rectangular a la pantalla.
        region = (x0, y0, x1, y1)
        
        Recorta el canvas interno y lo envía con coordenadas de origen.
        Si el daemon no soporta offset, usa push_full_screen() como fallback.
        """
        x0, y0, x1, y1 = region
        crop = self.image.crop((x0, y0, x1, y1))
        self._save_bmp_sync(crop, self.bmp_region)
        # El comando IMG acepta coordenada de destino: IMG x y archivo
        self._send_cmd(f"IMG {x0} {y0} {self.bmp_region}", post_delay=0.05)

    def push_header(self):
        self.push_region(self.REGION_HEADER)

    def push_body(self):
        self.push_region(self.REGION_BODY)

    def push_footer(self):
        self.push_region(self.REGION_FOOTER)