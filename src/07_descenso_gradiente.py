import pandas as pd
import numpy as np
from tabulate import tabulate
import os

CARPETA = os.path.dirname(os.path.realpath(__file__)) + "\\..\\data\\" #no se modifica

# 1. Cargar el dataset normalizado
df = pd.read_csv(CARPETA + "03_dataset_normalizado.csv")

# Seleccionar 3 eventos específicos para entrenar (ej. 2 normales y 1 ataque)
# Índices 0 y 1 suelen ser 'Normal', el índice 278 (en este caso) era 'Ataque (nmap)'
eventos_idx = [0, 1, df[df["Escenario"] == "Ataque (nmap)"].index[0]]
datos_entrenamiento = df.iloc[eventos_idx]

# 2. Valores iniciales
w = np.array([2.5, 2.5, 0.0, 0.0])
b = -2.0
alpha = 0.1  # Tasa de aprendizaje

evolucion = []

print("Iniciando Descenso del Gradiente...\n")

# 3. Iterar sobre los 3 eventos
for i, (_, fila) in enumerate(datos_entrenamiento.iterrows(), 1):
    # Vector x (características)
    x = np.array([fila["Bytes/s"], fila["Paquetes/s"], fila["Temp"], fila["Duración"]])

    # Valor real (y): 1 si es Ataque, 0 si es Normal
    y = 1 if "Ataque" in fila["Escenario"] else 0

    # Calcular z y sigma(z) (predicción y_hat)
    z = np.dot(w, x) + b
    y_hat = 1 / (1 + np.exp(-z))

    # Calcular el error
    error = y_hat - y

    # Calcular gradientes: (y_hat - y) * x
    grad_w = error * x
    grad_b = error

    # Guardar estado actual antes de actualizar
    evolucion.append(
        {
            "Iteración": i,
            "Escenario": fila["Escenario"],
            "y_real": y,
            "y_prediccion": round(y_hat, 4),
            "w1 (Bytes)": round(w[0], 4),
            "w2 (Paquetes)": round(w[1], 4),
            "w3 (Temp)": round(w[2], 4),
            "w4 (Dur)": round(w[3], 4),
            "b (Sesgo)": round(b, 4),
        }
    )

    # Actualizar pesos: w = w - alpha * gradiente [cite: 135]
    w = w - alpha * grad_w
    b = b - alpha * grad_b

# Guardar el estado final tras la 3ra iteración
evolucion.append(
    {
        "Iteración": "Final",
        "Escenario": "-",
        "y_real": "-",
        "y_prediccion": "-",
        "w1 (Bytes)": round(w[0], 4),
        "w2 (Paquetes)": round(w[1], 4),
        "w3 (Temp)": round(w[2], 4),
        "w4 (Dur)": round(w[3], 4),
        "b (Sesgo)": round(b, 4),
    }
)

# 4. Mostrar EVIDENCIA OBLIGATORIA
df_evolucion = pd.DataFrame(evolucion)
df_evolucion.to_csv(CARPETA + "\\..\\evidencias\\" + "07_evidencia_evolucion_pesos.csv", index=False)

print("--- EVIDENCIA: EVOLUCIÓN DE PESOS (3 ITERACIONES) ---")
print(tabulate(df_evolucion, headers="keys", tablefmt="pipe", showindex=False))
