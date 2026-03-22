import pyshark
import pandas as pd
import binascii
import json
import os


CARPETA = os.path.dirname(os.path.realpath(__file__)) + "\\..\\data\\" #no se modifica
ARCHIVO = "01_archivo.pcapng" # Solo nombre del archivo en la carpeta 'data'


def generar_dataset():
    print(f"Leyendo {ARCHIVO} (esto puede tardar un minuto)...")
    captura = pyshark.FileCapture(CARPETA + ARCHIVO)
    
    
    eventos = []
    tiempo_inicio = None

    # Contadores para la ventana actual (1 segundo = d)
    bytes_sec = 0
    paquetes_sec = 0
    temp_actual = 23.81  # Valor base por si el segundo no tiene lecturas IoT
    ventana_actual = 0

    for paquete in captura:
        try:
            tiempo_paquete = float(paquete.sniff_timestamp)
            if tiempo_inicio is None:
                tiempo_inicio = tiempo_paquete

            segundo_relativo = int(tiempo_paquete - tiempo_inicio)

            # Si cambiamos de segundo, guardamos el evento anterior
            if segundo_relativo > ventana_actual:
                # Clasificación automática del escenario
                if paquetes_sec > 1000:
                    escenario = "Ataque (nmap)"
                elif paquetes_sec > 50:
                    escenario = "Estrés"
                else:
                    escenario = "Normal"

                eventos.append(
                    {
                        "Evento": ventana_actual + 1,
                        "Bytes/s": bytes_sec,
                        "Paquetes/s": paquetes_sec,
                        "Temp": temp_actual,
                        "Duración": 1.0,
                        "Escenario": escenario,
                    }
                )

                # Reiniciar contadores
                bytes_sec = 0
                paquetes_sec = 0
                ventana_actual = segundo_relativo

            # Acumular tráfico general
            bytes_sec += int(paquete.length)
            paquetes_sec += 1

            # Extraer variable IoT (t) si es un paquete UDP de tu sensor
            if "UDP" in paquete and hasattr(paquete, "data"):
                hex_data = paquete.data.data.replace(":", "")
                try:
                    payload = binascii.unhexlify(hex_data).decode("utf-8")
                    datos = json.loads(payload)
                    if "temperatura" in datos:
                        temp_actual = datos["temperatura"]
                except:
                    pass  # Ignorar paquetes que no sean JSON válidos

        except AttributeError:
            continue

    captura.close()

    df = pd.DataFrame(eventos)

    # Asegurar el mínimo de 30 eventos requerido
    print(f"\nTotal de eventos procesados: {len(df)}")
    if len(df) < 30:
        print("¡Advertencia! Tienes menos de 30 eventos.")

    df.to_csv(CARPETA + "02_dataset_auquatrans.csv", index=False)
    print("\nPrimeras 5 filas del dataset generado:")
    print(df.head())

    return df


if __name__ == "__main__":
    generar_dataset()
