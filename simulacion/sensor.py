import socket
import time
import random
import sys
import json
from datetime import datetime

UDP_IP = "servidor"
UDP_PORT = 5005
MODO = sys.argv[1] if len(sys.argv) > 1 else "normal"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Iniciando sensor Auquatrans en modo: {MODO}")

while True:
    # Mantenemos los enteros intactos y randomizamos levemente los decimales
    temperatura = 23 + round(random.uniform(0.75, 0.85), 2)  # Ej. 23.81
    tds = 361 + round(random.uniform(0.40, 0.60), 2)  # Ej. 361.51
    salinidad = 0 + round(random.uniform(0.30, 0.40), 2)  # Ej. 0.36
    volt_ph = 1524 + round(random.uniform(0.50, 0.90), 2)  # Ej. 1524.85
    ph = 6 + round(random.uniform(0.40, 0.80), 2)  # Ej. 6.72

    payload = {
        "marca_tiempo": datetime.now().isoformat(),
        "temperatura": temperatura,
        "tds": tds,
        "salinidad": salinidad,
        "volt_ph": volt_ph,
        "ph": ph,
    }

    mensaje = json.dumps(payload)
    sock.sendto(mensaje.encode("utf-8"), (UDP_IP, UDP_PORT))

    if MODO == "normal":
        time.sleep(1)  # 1 envío por segundo
    elif MODO == "estres":
        time.sleep(0.01)  # 100 envíos por segundo para saturar la red
