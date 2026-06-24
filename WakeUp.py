from time import sleep
from wakeonlan import send_magic_packet
import platform
import subprocess

def wake_up_server(mac_address, ip_address, broadcast_ip):
    try_count = 0
    max_attempts = 10

    if is_reachable(ip_address):
        print(f"Server at {ip_address} is already up.")
        return True

    while not is_reachable(ip_address) and try_count < max_attempts:
        print(f"Server at {ip_address} is not reachable. Attempting to wake up (try {try_count + 1})...")
        
        try:
            send_magic_packet(mac_address, ip_address=broadcast_ip)
            print(f"Magic packet sent to {mac_address} via {broadcast_ip}")
        except Exception as e:
            print(f"Socket error: {e}. Retrying in 5 seconds...")
            
        sleep(5)
        try_count += 1

    if is_reachable(ip_address):
        print(f"Server at {ip_address} is now up.")
        return True
    else:
        print(f"Failed to wake up server at {ip_address} after {try_count} attempts.")
        return False

def is_reachable(ip_address):
    p = platform.system().lower()
    if p == 'windows':
        command = ['ping', '-n', '1', '-w', '1000', ip_address]
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        return result.returncode == 0 and "ttl=" in result.stdout.lower()
    else:
        command = ['ping', '-c', '1', '-W', '1', ip_address]
        result = subprocess.run(command, stdout=subprocess.DEVNULL, text=True)
        return result.returncode == 0

