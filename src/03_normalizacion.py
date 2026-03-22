import pandas as pd
import os

CARPETA = os.path.dirname(os.path.realpath(__file__)) + "\\..\\data\\" #no se modifica

# Cargar el dataset que acabas de generar
df = pd.read_csv(CARPETA + "02_dataset_auquatrans.csv")

# Seleccionar solo las columnas numéricas de nuestro vector x = (b, p, t, d)
columnas_vector = ["Bytes/s", "Paquetes/s", "Temp", "Duración"]
df_vector = df[columnas_vector]

# Aplicar la normalización z-score: x' = (x - mu) / sigma
# Nota: Si 'Duración' es siempre 1.0, su desviación estándar es 0.
# Pandas pondrá NaN (Not a Number) al dividir entre 0, así que lo rellenamos con 0.
df_normalizado = (df_vector - df_vector.mean()) / df_vector.std()
df_normalizado["Duración"] = df_normalizado["Duración"].fillna(0)

# Unimos las columnas de contexto (Evento y Escenario) para no perderlas
df_final = pd.concat([df[["Evento", "Escenario"]], df_normalizado], axis=1)

# Guardar el nuevo dataset
df_final.to_csv(CARPETA + "03_dataset_normalizado.csv", index=False)

print("--- TABLA ORIGINAL (Primeras 3 filas) ---")
print(df[["Evento", "Bytes/s", "Paquetes/s", "Temp", "Duración"]].head(3))
print("\n--- TABLA NORMALIZADA (Primeras 3 filas) ---")
print(df_final[["Evento", "Bytes/s", "Paquetes/s", "Temp", "Duración"]].head(3))
