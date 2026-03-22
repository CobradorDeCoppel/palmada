import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 1. Cargar los datos normalizados
df = pd.read_csv("dataset_normalizado.csv")
columnas_vector = ["Bytes/s", "Paquetes/s", "Temp", "Duración"]
X = df[columnas_vector]

# 2. Aplicar k-means con k=2
kmeans2 = KMeans(n_clusters=2, random_state=42, n_init=10)
df["Cluster_k2"] = kmeans2.fit_predict(X)
centroides_k2 = kmeans2.cluster_centers_

# 3. Aplicar k-means con k=3
kmeans3 = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster_k3"] = kmeans3.fit_predict(X)
centroides_k3 = kmeans3.cluster_centers_

# Guardar la tabla con los clusters asignados
df.to_csv("dataset_con_clusters.csv", index=False)

# Imprimir las evidencias obligatorias
print("--- EVIDENCIA: CENTROIDES FINALES (k=2) ---")
print(pd.DataFrame(centroides_k2, columns=columnas_vector))
print("\n--- EVIDENCIA: CENTROIDES FINALES (k=3) ---")
print(pd.DataFrame(centroides_k3, columns=columnas_vector))

# 4. EVIDENCIA: Gráfica de agrupamiento comparativa
# Graficaremos Bytes/s vs Paquetes/s ya que son las variables que más cambian en un ataque
plt.figure(figsize=(14, 6))

# Subplot para k=2
plt.subplot(1, 2, 1)
scatter2 = plt.scatter(
    df["Bytes/s"], df["Paquetes/s"], c=df["Cluster_k2"], cmap="viridis", alpha=0.7
)
plt.scatter(
    centroides_k2[:, 0],
    centroides_k2[:, 1],
    c="red",
    marker="X",
    s=200,
    label="Centroides",
)
plt.title("Agrupamiento k-means (k=2)")
plt.xlabel("Bytes/s (Normalizado)")
plt.ylabel("Paquetes/s (Normalizado)")
plt.legend()
plt.grid(True, linestyle=":", alpha=0.6)

# Subplot para k=3
plt.subplot(1, 2, 2)
scatter3 = plt.scatter(
    df["Bytes/s"], df["Paquetes/s"], c=df["Cluster_k3"], cmap="plasma", alpha=0.7
)
plt.scatter(
    centroides_k3[:, 0],
    centroides_k3[:, 1],
    c="red",
    marker="X",
    s=200,
    label="Centroides",
)
plt.title("Agrupamiento k-means (k=3)")
plt.xlabel("Bytes/s (Normalizado)")
plt.ylabel("Paquetes/s (Normalizado)")
plt.legend()
plt.grid(True, linestyle=":", alpha=0.6)

plt.tight_layout()
plt.savefig("grafica_kmeans_comparativa.png", dpi=300)
print("\n¡Gráfica 'evidencias/grafica_kmeans_comparativa.png' generada con éxito!")
