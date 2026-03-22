import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

CARPETA = os.path.dirname(os.path.realpath(__file__)) + "\\..\\data\\" #no se modifica
# 1. Cargar los datos

df_orig = pd.read_csv(CARPETA + "02_dataset_auquatrans.csv")
df_norm = pd.read_csv(CARPETA + "03_dataset_normalizado.csv")

columnas_vector = ["Bytes/s", "Paquetes/s", "Temp", "Duración"]

# 2. Calcular centroide del comportamiento normal
# Filtramos solo los eventos normales y calculamos el promedio de sus características
datos_normales = df_norm[df_norm["Escenario"] == "Normal"][columnas_vector]
vector_centroide = datos_normales.mean().values

print("--- EVIDENCIA 1: VECTOR CENTROIDE ---")
print(f"c = {vector_centroide}\n")

# 3. Calcular distancias para todos los eventos
# Usamos álgebra lineal de numpy para calcular la distancia euclidiana de cada fila al centroide
distancias = np.linalg.norm(df_norm[columnas_vector].values - vector_centroide, axis=1)

# Agregamos la distancia al dataframe para tener la tabla
df_orig["Distancia_al_Centroide"] = distancias

print("--- EVIDENCIA 2: TABLA DE DISTANCIAS (Muestra) ---")
print(df_orig[["Evento", "Escenario", "Distancia_al_Centroide"]].head(10))
df_orig.to_csv(CARPETA + "..\\evidencias\\" +
    "04_tabla_distancias_final.csv", index=False
)  # Guardamos la evidencia completa

# 4. Definir umbral de anomalía
# Un buen umbral empírico es el valor máximo de distancia que alcanzó el tráfico "Normal" más un margen del 10%
distancia_max_normal = df_orig[df_orig["Escenario"] == "Normal"][
    "Distancia_al_Centroide"
].max()
umbral = distancia_max_normal * 1.10

print(f"\nUmbral de anomalía definido en: {umbral:.4f}")

# 5. EVIDENCIA 3: Gráfica distancia vs evento
plt.figure(figsize=(12, 6))

# Colorear según el escenario real para ver si el umbral hace sentido
colores = {"Normal": "green", "Estrés": "orange", "Ataque (nmap)": "red"}
for escenario in df_orig["Escenario"].unique():
    subset = df_orig[df_orig["Escenario"] == escenario]
    plt.scatter(
        subset["Evento"],
        subset["Distancia_al_Centroide"],
        label=escenario,
        c=colores.get(escenario, "blue"),
        alpha=0.7,
    )

# Dibujar la línea del umbral
plt.axhline(
    y=umbral, color="red", linestyle="--", label=f"Umbral Anomalía ({umbral:.2f})"
)

plt.title("Distancia al Centroide Normal vs Eventos en el Tiempo")
plt.xlabel("Evento (Segundos)")
plt.ylabel("Distancia Euclidiana")
plt.legend()
plt.grid(True, linestyle=":", alpha=0.6)

# Guardar la gráfica para el anexo
plt.savefig(CARPETA + "\\..\\evidencias\\" + "04_grafica_distancias.png", dpi=300, bbox_inches="tight")
print("\n¡Tabla 'data/04_tabla_distancias_final.csv' generada!")
print("\n¡Gráfica 'evidencias/04_grafica_distancias.png' generada!")
