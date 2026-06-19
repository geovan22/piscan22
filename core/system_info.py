# core/system_info.py
import psutil
import subprocess
import os

class SystemMonitor:
    def get_cpu(self):
        return f"{int(psutil.cpu_percent())}%"

    def get_ram(self):
        return f"{int(psutil.virtual_memory().percent)}%"

    def get_temp(self):
        try:
            res = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
            return res.stdout.replace("temp=", "").replace("'C\n", "C").split('.')[0] + "C"
        except Exception:
            return "N/A"

    def get_network_type(self):
        """Devuelve 'wifi', 'lan', o 'disconnected' leyendo el kernel de Linux"""
        try:
            # Chequear conexión física LAN (eth0)
            if os.path.exists("/sys/class/net/eth0/carrier"):
                with open("/sys/class/net/eth0/carrier") as f:
                    if f.read().strip() == "1":
                        return "lan"
            # Chequear conexión WiFi (wlan0)
            if os.path.exists("/sys/class/net/wlan0/carrier"):
                with open("/sys/class/net/wlan0/carrier") as f:
                    if f.read().strip() == "1":
                        return "wifi"
        except:
            pass
        return "disconnected"

    def get_battery(self):
        """
        Devuelve el nivel de batería. 
        [TODO]: Conectar a lectura real de hardware por I2C (ej. módulo de carga o ADS1115).
        """
        # Valor quemado al 100% temporalmente
        return 100