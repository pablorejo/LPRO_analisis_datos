import pandas as pd
from datetime import datetime

from minisom import MiniSom
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns; sns.set()  # para visualización bonita

resolucion = 5
iteraciones = 3000
def fecha_hora_a_entero(fecha_hora_str):
    """
    Convierte una fecha y hora en formato string a un número entero.
    
    Parámetros:
    - fecha_hora_str (str): La fecha y hora en formato string, esperado en el formato "AAAA-MM-DD HH:MM:SS.ssssss".
    
    Retorna:
    - int: Un número entero que representa la fecha y hora.
    """
    # Convertir la cadena de fecha y hora a un objeto datetime
    fecha_hora = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M:%S.%f")
    
    # Convertir la fecha y hora a un número entero (formato AAAAMMDDHHMMSS)
    fecha_hora_entero = int(fecha_hora.strftime("%Y%m%d%H%M%S"))
    
    return fecha_hora_entero
    

df_datos = pd.read_csv('datos.csv')

df_datos['fecha'] = df_datos['fecha'].apply(fecha_hora_a_entero)
X = df_datos[['longitud','fecha']].values


# Supongamos que X es tu conjunto de datos con dimensiones (n_muestras, n_caracteristicas)
# X = ...

# Normalizar los datos
X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

# Crear el SOM
# Los parámetros x y y definen el tamaño del grid del SOM. sigma es el radio de la vecindad. learning_rate es la tasa de aprendizaje.
som = MiniSom(x=resolucion, y=resolucion, input_len=X.shape[1], sigma=0.3, learning_rate=0.3)

# Inicializar los pesos
som.random_weights_init(X)

# Entrenar el SOM
som.train_random(X, num_iteration=iteraciones)

# Ahora el SOM está entrenado y puedes usarlo para mapear los datos a su espacio 2D o para visualizar los patrones aprendidos.



# Calcular la distancia de cada punto a su BMU
distancias_a_bmu = np.array([np.linalg.norm(x-som.get_weights()[som.winner(x)]) for x in X])

# Establecer un umbral, por ejemplo, el percentil 90
umbral = np.percentile(distancias_a_bmu, 90)

# Identificar las anomalías
anomalias = distancias_a_bmu > umbral

# Contar y imprimir el número de anomalías
n_anomalias = np.sum(anomalias)
print(f'Número total de anomalías detectadas: {n_anomalias}')

# Calcular la matriz de confusión
matriz_conf = confusion_matrix(df_datos['anomalia'], anomalias)

# Visualizar la matriz de confusión
plt.figure(figsize=(10,7))
sns.heatmap(matriz_conf, annot=True, fmt='d',
            xticklabels=['No anomalia', 'anomalia'],
            yticklabels=['No anomalia', 'anomalia'])
plt.ylabel('Valores de prediccion')
plt.xlabel('Valores reales')
plt.show()

# Ahora `anomalias` es un arreglo booleano donde True indica una anomalía

