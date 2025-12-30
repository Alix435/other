from datetime import datetime
import platform
import subprocess
import re


# class IPMonitor:
#     def __init__(self):
#         self.ip_addresses = []

# ----------------------------------------------------------------------------------------------------------------------
# Ping ip address
def ping_ip(ip_info):
    try:
        ip = ip_info['ip_address']
        if platform.system().lower() == "windows":
            command = ["ping", "-n", "2", "-w", "2000", ip]
        else:
            command = ["ping", "-c", "2", "-W", "2", ip]

        result = subprocess.run(command, capture_output=True, text=True, timeout=5)

        now = datetime.now().strftime("%H:%M:%S")
        if result.returncode == 0:
            time_match = re.search(r'time=([\d.]+)\s*ms', result.stdout)
            if not time_match and platform.system().lower() == "windows":
                time_match = re.search(r'Average = (\d+)ms', result.stdout)

            response_time = float(time_match.group(1)) if time_match else 0

            ip_info['status'] = True
            ip_info['response_time'] = round(response_time, 2)
            ip_info['last_check'] = now
        else:
            ip_info['status'] = False
            ip_info['response_time'] = 0
            ip_info['last_check'] = now

    except Exception as e:
        ip_info['status'] = False
        ip_info['response_time'] = 0
        ip_info['last_check'] = datetime.now().strftime("%H:%M:%S")

    return ip_info




