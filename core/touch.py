# core/touch.py - Controlador de pantalla táctil para PiScan
import spidev

class TouchScreen:
    def __init__(self, bus=0, device=1): # device=1 (CE1)
        self.bus = bus
        self.device = device
        
    def get_touch(self):
        # Abrimos y cerramos la conexión SPI en cada lectura 
        # para garantizar que no bloqueamos el demonio de video en C.
        try:
            spi = spidev.SpiDev()
            spi.open(self.bus, self.device)
            spi.max_speed_hz = 50000 
            
            resp_x = spi.xfer2([0xD0, 0x00, 0x00])
            resp_y = spi.xfer2([0x90, 0x00, 0x00])
            
            spi.close() # ¡LIBERACIÓN INMEDIATA DEL BUS!
            
            x_raw = ((resp_x[1] << 8) | resp_x[2]) >> 3
            y_raw = ((resp_y[1] << 8) | resp_y[2]) >> 3
            
            if x_raw < 200 or y_raw < 200 or x_raw > 3900 or y_raw > 3900:
                return None
                
            # Calibración
            pixel_x = int((x_raw - 200) / (3800 - 200) * 480)
            pixel_y = int((y_raw - 200) / (3800 - 200) * 320)
            
            return (pixel_x, pixel_y)
        except:
            return None