import spidev
import time

class TouchScreen:
    def __init__(self, bus=0, device=1):
        """Inicializa la conexión SPI con el controlador táctil"""
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(bus, device)
            self.spi.max_speed_hz = 50000  # Velocidad súper segura para la Raspberry Pi 1
            self.spi.no_cs = False
        except Exception as e:
            print(f"[ERROR TACTIL] No se pudo iniciar el bus SPI: {e}")
            self.spi = None

    def get_touch(self):
        """Lee el panel táctil y traduce la lectura a resolución 480x320"""
        if not self.spi:
            return None
        
        try:
            # Enviar los comandos en hexadecimal para leer el eje X (0xD0) y el eje Y (0x90)
            resp_x = self.spi.xfer2([0xD0, 0x00, 0x00])
            resp_y = self.spi.xfer2([0x90, 0x00, 0x00])
            
            # El chip táctil responde con 3 bytes. Hacemos la matemática de bits
            # para convertir eso en un número del 0 al 4095 (12-bit ADC)
            x_raw = ((resp_x[1] << 8) | resp_x[2]) >> 3
            y_raw = ((resp_y[1] << 8) | resp_y[2]) >> 3
            
            # Si los valores son muy extremos, significa que no hay dedo en la pantalla
            if x_raw < 200 or y_raw < 200 or x_raw > 3900 or y_raw > 3900:
                return None
                
            # --- CALIBRACIÓN MATEMÁTICA ---
            # Mapeamos los valores eléctricos (200 a 3800) a tus píxeles (0 a 480 y 0 a 320)
            pixel_x = int((x_raw - 200) / (3800 - 200) * 480)
            pixel_y = int((y_raw - 200) / (3800 - 200) * 320)
            
            # Limitamos los valores para que nunca devuelva coordenadas fuera de la pantalla
            pixel_x = max(0, min(480, pixel_x))
            pixel_y = max(0, min(320, pixel_y))
            
            return (pixel_x, pixel_y)
            
        except Exception as e:
            return None