# core/system_info.py
import psutil
import subprocess
import socket

class SystemMonitor:
    def get_cpu(self):
        """Devuelve el uso de CPU en porcentaje"""
        return f"{int(psutil.cpu_percent())}%"

    def get_ram(self):
        """Devuelve el uso de RAM en porcentaje"""
        return f"{int(psutil.virtual_memory().percent)}%"

    def get_temp(self):
        """Lee la temperatura del procesador de la Raspberry Pi"""
        try:
            # Intento nativo para Raspberry Pi
            res = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
            # Limpiar salida (ej. "temp=45.0'C" -> "45C")
            temp = res.stdout.replace("temp=", "").replace("'C\n", "C").split('.')[0] + "C"
            return temp
        except Exception:
            return "N/A"

    def is_connected(self):
        """Revisa si hay conexión a internet haciendo un ping rápido a un DNS"""
        try:
            socket.setdefaulttimeout(1)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            return True
        except OSError:
            return False
        
    # ... código anterior de get_temp y is_connected ...

    def get_battery(self):
        """
        Devuelve el nivel de batería. 
        [TODO]: Conectar a lectura real de hardware por I2C (ej. INA219 o ADS1115).
        """
        return 100