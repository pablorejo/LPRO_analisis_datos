import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd
import json
import random
MOSTRAR_GRAFICO = True
# Ejemplo de datos: coordenadas [latitud, longitud]
data_df = pd.read_csv('datos.csv')
data_df = data_df[['latitude', 'longitude']]
points = data_df.to_numpy()



def random_subsampling(points, sample_size):
    """ Reduce el número de puntos mediante submuestreo aleatorio.
    
    Args:
    points (list of tuples): Lista de puntos (latitud, longitud).
    sample_size (int): Número de puntos a seleccionar.
    
    Returns:
    list of tuples: Lista reducida de puntos.
    """
    # Convertir el array de NumPy a lista de tuplas
    points_list = [tuple(point) for point in points]
    if sample_size >= len(points_list):
        return points_list
    sampled_points = random.sample(points_list, sample_size)
    return sampled_points


    
points_reduce = random_subsampling(points, 300)

# Convertir la lista de tuplas nuevamente a DataFrame
reduced_df = pd.DataFrame(points_reduce, columns=['latitude', 'longitude'])

# Convertir el DataFrame a un diccionario y luego a JSON
clusters_json = reduced_df.to_dict(orient='records')
json_output = json.dumps(clusters_json, indent=4)

with open('fichero.json','w') as file:
    file.write(json_output)
    file.close()
print(json_output)