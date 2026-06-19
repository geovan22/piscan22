import spidev

class TouchScreen:
    def __init__(self, bus=0, device=1):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 50000 
        
    def get_touch(self):
        try:
            resp_x = self.spi.xfer2([0xD0, 0x00, 0x00])
            resp_y = self.spi.xfer2([0x90, 0x00, 0x00])
            
            x_raw = ((resp_x[1] << 8) | resp_x[2]) >> 3
            y_raw = ((resp_y[1] << 8) | resp_y[2]) >> 3
            
            if x_raw < 200 or y_raw < 200 or x_raw > 3900 or y_raw > 3900:
                return None
                
            pixel_x = int((x_raw - 200) / (3800 - 200) * 480)
            pixel_y = int((y_raw - 200) / (3800 - 200) * 320)
            
            return (pixel_x, pixel_y)
        except:
            return None