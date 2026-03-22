import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Cargar datos
df = pd.read_csv("dataset_con_clusters.csv")  # Usamos el que ya tiene k-means
X_cols = ["Bytes/s", "Paquetes/s", "Temp", "Duración"]
X = df[X_cols].values

# Crear etiqueta 'y' real para el entrenamiento del error (1 si es Ataque, 0 si no)
y_real = np.where(df["Escenario"] == "Ataque (nmap)", 1, 0)

# 2. Mini-entrenamiento para la evolución del error (50 iteraciones)
w = np.array([2.5, 2.5, 0.0, 0.0])  # Pesos iniciales justificados
b = -2.0
alpha = 0.05
errores_historial = []

for epoca in range(50):
    # Predicción de todo el batch
    z = np.dot(X, w) + b
    y_pred = 1 / (1 + np.exp(-z))

    # Calcular el error medio absoluto (MAE) de esta época
    error_medio = np.mean(np.abs(y_pred - y_real))
    errores_historial.append(error_medio)

    # Actualizar pesos (Gradiente Descendente Batch)
    grad_w = np.dot((y_pred - y_real), X) / len(X)
    grad_b = np.mean(y_pred - y_real)

    w = w - alpha * grad_w
    b = b - alpha * grad_b

# 3. CREAR LAS GRÁFICAS (Visualización Avanzada)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# --- GRÁFICA 1: Clusters 2D + Frontera de Decisión ---
# Dibujamos los puntos en 2D (Bytes vs Paquetes) coloreados por el cluster k=2
scatter = ax1.scatter(
    df["Bytes/s"],
    df["Paquetes/s"],
    c=df["Cluster_k2"],
    cmap="coolwarm",
    alpha=0.8,
    edgecolors="k",
)

# Calcular la línea de la frontera de decisión: w1*x1 + w2*x2 + b = 0  =>  x2 = -(w1/w2)x1 - (b/w2)
x_vals = np.array([df["Bytes/s"].min(), df["Bytes/s"].max()])
y_vals = -(w[0] / w[1]) * x_vals - (b / w[1])

ax1.plot(
    x_vals,
    y_vals,
    "--",
    color="black",
    linewidth=2,
    label="Frontera de Decisión (Modelo Lineal)",
)

ax1.set_title("Agrupamiento K-means y Frontera de Decisión (Bytes vs Paquetes)")
ax1.set_xlabel("Bytes/s (Normalizado)")
ax1.set_ylabel("Paquetes/s (Normalizado)")
ax1.legend()
ax1.grid(True, linestyle=":", alpha=0.6)

# --- GRÁFICA 2: Evolución del Error ---
ax2.plot(
    range(1, 51),
    errores_historial,
    color="purple",
    linewidth=2.5,
    marker="o",
    markersize=4,
)
ax2.set_title("Evolución del Error (Descenso del Gradiente)")
ax2.set_xlabel("Iteración (Época)")
ax2.set_ylabel("Error Medio Absoluto")
ax2.grid(True, linestyle=":", alpha=0.6)

# Ajustar y guardar
plt.tight_layout()
plt.savefig("evidencia_visualizacion_avanzada.png", dpi=300)
print(
    "¡Visualización avanzada completada! Gráfica guardada como 'evidencias/08_evidencia_visualizacion_avanzada.png'."
)
