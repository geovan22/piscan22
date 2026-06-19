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
            res = subprocess.run(
                ['vcgencmd', 'measure_temp'],
                capture_output=True, text=True, timeout=2
            )
            # "temp=42.5'C" → "42C"
            return res.stdout.replace("temp=", "").split(".")[0] + "C"
        except Exception:
            return "N/A"

    def get_network_type(self):
        """
        Devuelve: 'wifi', 'lan', o 'disconnected'
        Leyendo /sys/class/net/ del kernel de Linux.
        """
        try:
            # LAN primero (eth0)
            carrier = "/sys/class/net/eth0/carrier"
            if os.path.exists(carrier):
                with open(carrier) as f:
                    if f.read().strip() == "1":
                        return "lan"
            # WiFi (wlan0)
            carrier = "/sys/class/net/wlan0/carrier"
            if os.path.exists(carrier):
                with open(carrier) as f:
                    if f.read().strip() == "1":
                        return "wifi"
        except Exception:
            pass
        return "disconnected"

    def get_battery(self):
        """
        [TODO] Conectar a lectura real de hardware por I2C (ej. ADS1115).
        Por ahora devuelve 100 como placeholder.
        """
        return 100