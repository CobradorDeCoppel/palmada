# Proyecto Auquatrans: IDS basado en Machine Learning

Este repositorio contiene la simulación, captura de tráfico y análisis matemático para un Sistema de Detección de Intrusos (IDS) diseñado para proteger la telemetría de la red IoT "Auquatrans". El proyecto implementa algoritmos de Machine Learning (K-means y Regresión Lineal con función Sigmoide) optimizados mediante el Descenso del Gradiente para detectar anomalías y ataques de red.

## ⚙️ Requisitos del Sistema e Instalación

Para ejecutar el análisis desde cero, se requiere un entorno Linux (testeado en Kubuntu 24.04 LTS) con Python 3 instalado.

1. Instalar la dependencia del sistema operativo necesaria para leer archivos `.pcapng`:
   sudo apt update && sudo apt install tshark

2. Instalar las dependencias de Python:
   pip install -r requirements.txt

## 📂 Estructura del Proyecto

El repositorio está organizado bajo el siguiente flujo de trabajo técnico:

.
├── README.md
├── requirements.txt
├── actualizar_rutas.sh           # Script bash (sed) para mantenimiento de rutas
├── simulacion/                   # Entorno virtualizado IoT
│   ├── docker-compose.yml        # Topología de red (Sensor, Servidor, Atacante)
│   ├── sensor.py                 # Generador de telemetría legítima y estrés
│   └── servidor.py               # Receptor UDP (puerto 5005)
├── data/                         # Datasets y evidencias de red crudas
│   ├── archivo.pcapng            # Captura completa del tráfico (Normal, Estrés, Nmap)
│   ├── dataset_auquatrans.csv    # Vector de características extraído
│   ├── dataset_normalizado.csv   # Dataset con normalización Z-Score
│   └── dataset_con_clusters.csv  # Dataset pre-etiquetado para visualización
├── src/                          # Scripts de análisis matemático y Machine Learning
│   ├── 02_procesar_pcap.py       # Extracción de características desde el .pcapng
│   ├── 03_normalizacion.py       # Aplicación de la fórmula de normalización
│   ├── 04_centroide_distancias.py# Cálculo de distancia euclidiana hacia el centroide normal
│   ├── 05_kmeans.py              # Clustering no supervisado comparando k=2 y k=3
│   ├── 06_modelo_lineal.py       # Clasificación binaria y función sigmoide
│   ├── 07_descenso_gradiente.py  # Optimización iterativa de pesos w1, w2, w3, w4 y b
│   └── 09_visualizacion_avanzada.py # Generación de gráfica de dispersión y evolución de error
└── evidencias/                   # Resultados, tablas y gráficas generadas
    ├── evidencia_evolucion_pesos.csv
    ├── evidencia_modelo_lineal.csv
    ├── evidencia_visualizacion_avanzada.png
    ├── grafica_distancias.png
    ├── grafica_kmeans_comparativa.png
    └── tabla_distancias_final.csv

## 🚀 Flujo de Ejecución del Análisis

Si se desea auditar o regenerar las evidencias matemáticas, los scripts dentro de la carpeta `src/` están numerados en orden de ejecución lógica. Se deben ejecutar desde la raíz del proyecto para mantener la integridad de las rutas relativas.

Ejemplo:
python3 src/02_procesar_pcap.py
python3 src/03_normalizacion.py
# ... continuar con el resto en orden numérico

## 🛡️ Vector de Ataque Analizado
Se inyectó una tormenta de paquetes simulando una fase de reconocimiento de red agresiva utilizando `nmap -p- -A`. El ataque generó miles de paquetes TCP por segundo, alterando drásticamente el vector matemático de características, lo cual es identificado por el modelo lineal cruzando la frontera de decisión en la probabilidad sigmoidal.
