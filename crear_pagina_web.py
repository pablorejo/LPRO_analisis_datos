from random import randint
import pandas as pd
import folium
from folium.plugins import HeatMap
from conf import *

def crar_figura_mapa(mapa: folium.Map,parcela: list):
    
    # Asegurándonos de que 'parcela' es una lista de tuplas (lat, lon)
    # y usamos folium.Polygon para parcelas de terreno con múltiples esquinas
    folium.Polygon(
        locations=parcela,  # Lista de puntos que definen la parcela
        color='#ff7800',
        fill=True,
        fill_color='#ffff00',
        fill_opacity=0.2
    ).add_to(mapa)
  

df = pd.read_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_DATOS))
def generar_color_aleatorio():
    # "#3388ff"
    randint(1, 16777215)
    color = '#' + str(hex(randint(1, 16777215))).split('x')[1]
    return color

print ("Datos guardados")


# Crea un mapa centrado en las coordenadas medias
mapa = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)

df_parcelas = pd.read_csv(path.join(CARPETA_DATOS_CSV,'parcelas.csv'))
# Organizar el DataFrame en una lista de listas de coordenadas por cada parcela
parcelas_dict = df_parcelas.groupby('id_parcela').apply(
    lambda x: list(zip(x.latitude, x.longitude))
).to_dict()

# Convertir el diccionario en una lista de parcelas, donde cada parcela es representada por su lista de coordenadas
parcelas = list(parcelas_dict.values())
    
    
for parcela in parcelas:
    crar_figura_mapa(mapa,parcela)
# Agrupa el DataFrame por 'Numero_pendiente'
colores = ['red', 'blue']
i = 0
for _, group in df.groupby('Numero_pendiente'):
    puntos = group[['latitude', 'longitude']].values
    # Añade los puntos al mapa
    folium.PolyLine(puntos, color=generar_color_aleatorio(), weight=2.5, opacity=1).add_to(mapa)
    
    for punto in puntos:
        # Crea un marcador con un popup que muestra el número
        folium.CircleMarker(location=punto, radius=5, color='blue', fill=True, 
                            popup=f'Punto {i}').add_to(mapa)
        i += 1  # Incrementa el contador para el siguiente punto
    
    i +=1


# Mostrar el mapa
mapa.save('mapa_de_posicion.html')

mapa = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)
for parcela in parcelas:
    crar_figura_mapa(mapa,parcela)
# Crear el mapa de calor
HeatMap(data=df[['latitude', 'longitude']].values, radius=15).add_to(mapa)

# Guardar el mapa en un archivo HTML
mapa.save('mapa_de_calor.html')