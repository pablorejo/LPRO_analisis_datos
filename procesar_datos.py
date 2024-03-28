# Vamos a procesar los datos obtenidos.
import pandas as pd
import numpy as np
from conf import *
from shapely.geometry import Point, Polygon

def haversine(lon1, lat1, lon2, lat2):
    """
    Calcula la distancia del círculo grande entre dos puntos en la Tierra.
    """
    # convertir grados decimales a radianes
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # fórmula haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371 # Radio de la Tierra en kilómetros. Usa 3956 para millas
    return c * r

# Cargar los datos desde el archivo CSV
data = pd.read_csv('datos.csv')

# Asegúrate de que la columna de fecha está en formato datetime

# Ordenar los datos por fecha
data = data.sort_values(by=['Numero pendiente', 'fecha'])

# Calcular la distancia y la velocidad
distancias = []
velocidades = []
fuera_de_parcela = []
data['fecha'] = pd.to_datetime(data['fecha'])

poligono_parcela = Polygon(parcelas[0])

for i in range(1, len(data)):
    row_prev = data.iloc[i-1]
    row = data.iloc[i]
    guardar = True
    
    try:
        guardar = row_prev['Numero pendiente'] == row['Numero pendiente'] 
    except: 
        guardar = False
    
    if (guardar):
        distancia = haversine(row_prev['longitude'], row_prev['latitude'], row['longitude'], row['latitude'])
        tiempo = ( row['fecha'] -row_prev['fecha']).total_seconds()  # Tiempo en horas
        velocidad = distancia * 1000 / tiempo if tiempo > 0 else 0
        distancias.append(distancia)
        velocidades.append(velocidad)
    else:
        velocidades.append(0)
        distancias.append(0)
        
    fuera_de_parcela.append(poligono_parcela.contains(Point(row_prev['latitude'],row_prev['longitude'])))
    

# Añadir la distancia y velocidad calculada al DataFrame (asumiendo la primera velocidad y distancia como 0)
data['distancia_en_Km'] = [0] + distancias
data['velocidad_en_m/s'] = [0] + velocidades

    
linea = data.iloc[len(data)-1]

fuera_de_parcela.append(poligono_parcela.contains(Point(linea['latitude'],linea['longitude'])))

data['fuera_del_recinto'] = fuera_de_parcela

# Calcular la distancia total recorrida
distancia_total = sum(distancias)
data.to_csv('datos_procesados.csv',index=False)
print(f"Distancia total recorrida: {distancia_total} km")
# Opcional: Guardar los resultados en un nuevo archivo CSV
# data.to_csv('ruta_a_tu_archivo_con_resultados.csv', index=False)
