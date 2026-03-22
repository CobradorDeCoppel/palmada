import socket
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Servidor Auquatrans escuchando en puerto 5005...")

while True:
    data, addr = sock.recvfrom(2048)
    try:
        lectura = json.loads(data.decode("utf-8"))
        print(
            f"[{lectura['marca_tiempo']}] Recibido -> Temp: {lectura['temperatura']} °C | TDS: {lectura['tds']} ppm | pH: {lectura['ph']}"
        )
    except json.JSONDecodeError:
        pass
