import pandas as pd
import numpy as np
from tabulate import tabulate
import os 

CARPETA = os.path.dirname(os.path.realpath(__file__)) + "\\..\\data\\" #no se modifica

# 1. Cargar el dataset normalizado
df = pd.read_csv(CARPETA + "03_dataset_normalizado.csv")

# 2. Definir los pesos (w) y el sesgo (b)
w = np.array([2.5, 2.5, 0.0, 0.0])
b = -2.0

# Extraer la matriz X con las 4 variables
X = df[["Bytes/s", "Paquetes/s", "Temp", "Duración"]].values

# 3. Calcular z = w * x + b
df["z"] = np.dot(X, w) + b

# 4. Aplicar la función sigmoide: sigma(z) = 1 / (1 + e^-z)
df["sigma(z)"] = 1 / (1 + np.exp(-df["z"]))

# 5. Clasificación (Si la probabilidad es >= 50% (0.5), es un ataque)
df["Clasificación"] = np.where(df["sigma(z)"] >= 0.5, "Anomalía", "Normal")

# 6. Preparar la evidencia
tabla_evidencia = df[["Evento", "Escenario", "z", "sigma(z)", "Clasificación"]]
tabla_evidencia.to_csv(CARPETA + "06_evidencia_modelo_lineal.csv", index=False)

print("\n--- EVIDENCIA: TABLA MODELO LINEAL + SIGMOIDE ---")
print("\nEjemplo de Tráfico Normal:")

print(
    tabulate(
        tabla_evidencia[tabla_evidencia["Escenario"] == "Normal"].head(3),
        headers="keys",
        tablefmt="pipe",
        showindex=False,
    )
)

print("\nEjemplo de Tráfico de Ataque:")
print(
    tabulate(
        tabla_evidencia[tabla_evidencia["Escenario"] == "Ataque (nmap)"].head(3),
        headers="keys",
        tablefmt="pipe",
        showindex=False,
    )
)
