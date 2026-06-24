import requests

def shutdown_server(ip_address,secret):
    try:
        payload = {"secret" : secret} if secret else {}
        response = requests.post(f"http://{ip_address}/shutdown", json=payload)
        if response.status_code == 200:
            print(f"Shutdown command sent to server at {ip_address}.")
        else:
            print(f"Failed to send shutdown command to server at {ip_address}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending shutdown command: {e}")