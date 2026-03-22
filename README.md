# Proyecto Auquatrans: IDS basado en Machine Learning

Este repositorio contiene la simulación, captura de tráfico y análisis matemático para un Sistema de Detección de Intrusos (IDS) diseñado para proteger la telemetría de la red IoT "Auquatrans". El proyecto implementa algoritmos de Machine Learning (K-means, Regresión Lineal con Sigmoide y Descenso del Gradiente) para detectar anomalías y ataques de red.

## ⚙️ Requisitos del Sistema e Instalación

Se requiere un entorno Linux con Python 3 instalado.

1. Instalar la dependencia del sistema operativo necesaria para leer archivos `.pcapng`:
   ```bash
   sudo apt update && sudo apt install tshark

    Instalar las dependencias de Python:
    Bash

    pip install -r requirements.txt

📂 Estructura del Proyecto

El repositorio está organizado en las siguientes categorías:
Archivos Base

    README.md: Documentación principal del proyecto.

    requirements.txt: Lista de dependencias de Python.

Virtualización IoT (simulacion/)

    docker-compose.yml: Topología de red (Sensor, Servidor, Atacante).

    sensor.py: Generador de telemetría legítima y estrés.

    servidor.py: Receptor UDP (puerto 5005).

Datos y Evidencias Crudas (data/)

    01_archivo.pcapng: Captura completa del tráfico (Normal, Estrés, Nmap).

    02_dataset_auquatrans.csv: Vector de características extraído de la red.

    03_dataset_normalizado.csv: Dataset con normalización Z-Score.

    05_dataset_con_clusters.csv: Dataset pre-etiquetado.

Código de Análisis (src/)

    02_procesar_pcap.py: Extracción de características desde el .pcapng.

    03_normalizacion.py: Aplicación de la fórmula de normalización Z-Score.

    04_centroide_distancias.py: Cálculo de distancia euclidiana hacia el centroide normal.

    05_kmeans.py: Clustering no supervisado comparando k=2 y k=3.

    06_modelo_lineal.py: Clasificación binaria y función sigmoide.

    07_descenso_gradiente.py: Optimización iterativa de pesos w y sesgo b.

    08_visualizacion_avanzada.py: Generación de gráficas de dispersión y evolución de error.

Resultados y Evidencias Visuales (evidencias/)

    04_tabla_distancias_final.csv: Tabla de distancias euclidianas.

    04_grafica_distancias.png: Gráfica de distancia al centroide en el tiempo.

    05_grafica_kmeans_comparativa.png: Comparación k-means (k=2 vs k=3).

    06_evidencia_modelo_lineal.csv: Resultados del modelo lineal y clasificación.

    07_evidencia_evolucion_pesos.csv: Histórico de actualización de pesos.

    08_evidencia_visualizacion_avanzada.png: Frontera de decisión y error.

🚀 Flujo de Ejecución del Análisis

Si se desea auditar o regenerar las evidencias matemáticas, los scripts dentro de la carpeta src/ deben ejecutarse secuencialmente desde la raíz del proyecto para mantener la integridad de las rutas relativas.

Ejemplo:
Bash

python3 src/02_procesar_pcap.py
python3 src/03_normalizacion.py
python3 src/04_centroide_distancias.py
# ... continuar con el resto en orden numérico

🛡️ Vector de Ataque Analizado

Se simuló un ataque de reconocimiento de red agresivo utilizando la herramienta nmap -p- -A desde un contenedor atacante. Esto inundó la red con paquetes TCP para escanear todos los puertos, alterando drásticamente las características de red (bytes y paquetes por segundo) en ventanas de 1 segundo, lo cual es identificado matemáticamente por el modelo cruzando la frontera de decisión sigmoide.
