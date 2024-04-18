from shapely.geometry import Polygon,Point
from geopy.distance import geodesic
from geographiclib.geodesic import Geodesic
import math
import json
from conf import obtener_coordenadas_parcela, obtener_coordenadas_sector, obtener_engine
import sys
from numpy import log2
import pandas as pd

def haversine(punto1, punto2):
    """
    Calcula la distancia entre el punto 1 y el 2
    """
    R = 6371.0
    lat1, lon1 = punto1
    lat2, lon2 = punto2
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calcular_area_esferica(coords):
    if len(coords) < 3:
        return 0
    # Comprobamos si el primer y último punto son diferentes, comparando cada elemento
    coords = coords + [coords[0]] if not all(c1 == c2 for c1, c2 in zip(coords[0], coords[-1])) else coords
    area = 0
    for i in range(len(coords) - 1):
        p1, p2 = coords[i], coords[i + 1]
        lat1, lon1 = map(math.radians, p1)
        lat2, lon2 = map(math.radians, p2)
        area += (lon2 - lon1) * (2 + math.sin(lat1) + math.sin(lat2))
    return abs(area) * (6371000 ** 2) / 2

def mover_punto(punto_inicio: tuple, punto_destino: tuple, distancia_metros: tuple):
    geod = Geodesic.WGS84.Inverse(*punto_inicio, *punto_destino)
    rumbo_inicial = geod['azi1']
    nuevo_punto = Geodesic.WGS84.Direct(punto_inicio[0], punto_inicio[1], rumbo_inicial, distancia_metros)
    return (nuevo_punto['lat2'], nuevo_punto['lon2'])

def esta_en_el_limite(punto, poligono):
    return Point(punto).touches(Polygon(poligono))

def punto_en_linea(punto: tuple, linea_punto1: tuple, linea_punto2: tuple, tolerancia=0.1):
    total_distancia = geodesic(linea_punto1, linea_punto2).meters
    dist_p1 = geodesic(punto, linea_punto1).meters
    dist_p2 = geodesic(punto, linea_punto2).meters
    return abs((dist_p1 + dist_p2) - total_distancia) <= tolerancia



def coordenadas_toca_parcela(coords_parcela: list,coords_subespacio: list):
    poligono_parcela = Polygon(coords_parcela)
    coords_subespacio_touch_parcela = {}

    for k in range(len(coords_subespacio)):
        if esta_en_el_limite(coords_subespacio[k],poligono_parcela):
            coords_subespacio_touch_parcela[k] = coords_subespacio[k]
    return coords_subespacio_touch_parcela



def seleccionar_coordenadas_desplazables(coords_subespacio_touch_parcela, coords_parcela):
    
    poligono_subespacio = Polygon(list(coords_subespacio_touch_parcela.values()))
    
    coordenadas_elegidas = {}
    # Precomputar límites para todas las coordenadas de la parcela
    en_limite = [esta_en_el_limite(coord, poligono_subespacio) for coord in coords_parcela]
    
    for i in range(len(coords_parcela)):
        actual = i
        previo = i - 1
        siguiente = previo if (en_limite[actual] and not en_limite[previo]) else actual
        anterior = actual if siguiente == previo else previo
        
        if en_limite[previo] != en_limite[actual]:
            coordenadas_posibles = {}
            for key, value in coords_subespacio_touch_parcela.items():
                if punto_en_linea(value, coords_parcela[anterior], coords_parcela[siguiente], 0):
                    coordenadas_posibles[key] = value
            
            menor_distancia = float('inf')
            index_elegido, coordenada_elegida = None, None
            for index, coordenada in coordenadas_posibles.items():
                dist = haversine(coordenada, coords_parcela[siguiente])
                if dist < menor_distancia:
                    menor_distancia = dist
                    coordenada_elegida = coordenada
                    index_elegido = index
            
            if index_elegido is not None:
                coordenadas_elegidas[index_elegido] = (coordenada_elegida, siguiente, anterior)
    
    return coordenadas_elegidas




def añadir_coordenadas_nuevas(coords_subespacio_touch_parcela: dict,coordeenadas_elegidas: dict):
    # Ajustar las coordenadas según las elecciones, modificando el índice si es necesario.
    for index, coordenada_tuple in coordeenadas_elegidas.items():
        siguiente, anterior = coordenada_tuple[1], coordenada_tuple[2]
        nuevo_index = index + 0.5 if siguiente < anterior else index - 0.5
        coords_subespacio_touch_parcela[nuevo_index] = coordenada_tuple[0]
    
    # Ordenar el diccionario por clave para asegurar consistencia.
    # Esto es importante si el orden de los índices afecta a la lógica de procesamiento posterior.
    coords_subespacio_touch_parcela = dict(sorted(coords_subespacio_touch_parcela.items()))

    return coords_subespacio_touch_parcela

    
def expandir_area(metros_cuadrados_expandir: int, coords_originales: list, coords_a_expandir: dict,coordeenadas_elegidas: dict, add_metros=5, num_maximo_bucle= 200):
    ADD_AREA = metros_cuadrados_expandir
    
    area_original = calcular_area_esferica(coords_originales)
    
    diferencia_area = 0
    coords_subespacio_sugerido = coords_a_expandir.copy()

    bucle = 0 
    while diferencia_area < ADD_AREA:
        for index, coordenada_tuple in coordeenadas_elegidas.items():
            siguiente = coordenada_tuple[1]
            anterior = coordenada_tuple[2]
            punto_bueno = True
            if not punto_en_linea(coords_subespacio_sugerido[index], coords_parcela[anterior], coords_parcela[siguiente], 1):
                if siguiente < anterior:
                    siguiente, anterior = max(0, siguiente - 1), siguiente
                else:
                    siguiente, anterior = min(len(coords_parcela) - 1, siguiente + 1), siguiente
                
                coords_subespacio_sugerido[index] = coords_parcela[siguiente]
                punto_bueno = False
                coordeenadas_elegidas[index] = coords_subespacio_sugerido[index], siguiente, anterior
                add_metros = 1

            if punto_bueno:
                coords_subespacio_sugerido[index] = mover_punto(coordenada_tuple[0], coords_parcela[siguiente], add_metros)
                
            nueva_area = calcular_area_esferica(list(coords_subespacio_sugerido.values()))
            diferencia_area = nueva_area - area_original
            
            if bucle > num_maximo_bucle:
                exit(ERROR_BUCLE_INFINITO)
            bucle += 1
            
            if diferencia_area - ADD_AREA >= 0:
                break
            else:
                add_metros += (ajustar_add_metros(diferencia_area, ADD_AREA))/2
       

    return coords_subespacio_sugerido

def ajustar_add_metros(diferencia_area, metros_cuadrados_expandir):
    if  diferencia_area > metros_cuadrados_expandir -50:
        return 3
    elif  diferencia_area > metros_cuadrados_expandir -300:
        return log2( metros_cuadrados_expandir - diferencia_area  + 1)/2
    else:
        return log2( metros_cuadrados_expandir - diferencia_area  + 1)

def verificar_argumentos():
    if len(sys.argv) < 3:
        print(json.dumps({"mensaje": "Algo ha salido mal"}))
        sys.exit(-1)
    return sys.argv[1], sys.argv[2]

def find_vertices(points):
    """Encuentra los vértices en una lista de puntos."""
    vertices = []
    n = len(points)
    for i in range(n):
        p1 = points[i - 1]  # punto anterior
        p2 = points[i]      # punto actual
        p3 = points[(i + 1) % n]  # punto siguiente, usando módulo para conectar el final con el principio
        
        if not punto_en_linea(p2, p1, p3):  # atol es la tolerancia, ajustar según la precisión deseada
            vertices.append(p2)
    
    return vertices


ERROR_NO_HAY_COORDENADAS_SUB_ESPACIO = -128
ERROR_BUCLE_INFINITO = -129


def obtener_recomendacion_sector(expansion_metros_cuadrados,porcentaje_de_error=0.1):
    IdUsuario,id_parcela = verificar_argumentos() # obtenemos los parametros 
    
    # Obtenemos las coordenadas de parcela y sector como array
    coords_subespacio = obtener_coordenadas_sector(id_parcela,True)
    coords_parcela = obtener_coordenadas_parcela(IdUsuario,id_parcela,True)
    ##
    
    # Reducimos quitando los puntos que estan en la linea que se une
    coords_parcela = find_vertices(coords_parcela)
    coords_subespacio = find_vertices(coords_subespacio)
    
    
    
    if len(coords_subespacio) == 0:
        exit(ERROR_NO_HAY_COORDENADAS_SUB_ESPACIO)
    
    ## Obtencion de las coordenadas
    coords_subespacio_touch_parcela = coordenadas_toca_parcela(coords_parcela,coords_subespacio) # Obtenemos las coordenadas del subespacio que toca la parcela
    
    
    
    coordeenadas_elegidas = seleccionar_coordenadas_desplazables(coords_subespacio_touch_parcela,coords_parcela) # Obtenemos las coordenadas que podemos desplazar
    
    
    coords_subespacio_touch_parcela_new = añadir_coordenadas_nuevas(coords_subespacio_touch_parcela,coordeenadas_elegidas) # Las añadimos a las coordenadas del subespacio a recomendar
    
    area_parcela = calcular_area_esferica(coords_parcela)
    expandir = expansion_metros_cuadrados - area_parcela * porcentaje_de_error
    coords_sugeridas = None
    
    # Comprobamos que el area a expadir es menor que el area total de la parcela
    if (expandir < area_parcela - calcular_area_esferica(coords_subespacio)):
        coords_sugeridas = coords_parcela
    else:
        coords_subespacio_sugerido = expandir_area(expansion_metros_cuadrados,coords_subespacio,coords_subespacio_touch_parcela_new,coordeenadas_elegidas)
        coords_sugeridas = find_vertices(list(coords_subespacio_sugerido.values()))

    return coords_sugeridas
    lista_de_diccionarios = [{'latitude': lat, 'longitude': lon} for lat, lon in coords_sugeridas]
    json_resultado = json.dumps(lista_de_diccionarios, indent=4)
    print(json_resultado)
    
    

# ******************************************************************* #
# ***************************** FUNCIONES *************************** # 
# ******************************************************************* #

# Función para el calculo del area de 
# parcelas y sectores a traves de coordenadas:
def calcular_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[i][1] * vertices[j][0]
    return abs(area) / 2

def calculoAreaSector(tiempoPastado, minPasto_m2):
    areaSector = tiempoPastado * (1/minPasto_m2)
    print("Área del Sector: ", areaSector, "m2")
    return areaSector








def getMinPastoVacas(cursor, idUsuario):
    consulta = "SELECT minPastoVaca \
                FROM Vaca \
                WHERE IdUsuario =" + str(idUsuario)

    cursor.execute(consulta)

    # Obtener los resultados de la consulta
    minPastoConsulta = cursor.fetchall()

    minPastoVaca = [tupla[0] for tupla in minPastoConsulta]

    minPasto = sum(minPastoVaca)
    return minPasto

    


if __name__ == "__main__":


    # Constantes calculo área pastada:
    minMetroCuadradoPastoMedio = 7.5	#min/m2
    minMetroCuadradoPastoPeorCaso = 5	#min/m2

    idusuario = 1
    numVacas = getVacas(cursor, idUsuario)
    #print(numVacas)

    coordenadas = obtener_coordenadas_parcela(idusuario, True) 
    print(coordenadas)

    areaParcela = calcular_area(coordenadas)
    areaParcela = 10**10*areaParcela

    print("El área del polígono es:", areaParcela, "m2")
    #print("El área del polígono es:", area1, "m2")

    # Crear un objeto de polígono Shapely para la extensión de tierra
    extencion_poligono = Polygon(coordenadas)

    # Calcular el centroide del polígono
    centroide = extencion_poligono.centroid

    # Calculo del área deseada para pastar:
    minPasto = getMinPastoVacas(cursor, idUsuario)
    areaSector = calculoAreaSector(minPasto, minMetroCuadradoPastoPeorCaso)

    # ************************************************** #
    # EXTRA: Calculo del area Pastada:
    areaPastada = calculoAreaSector(minPasto, minMetroCuadradoPastoMedio)
    areaParcelaRestante = areaParcela - (areaSector)
    print("Área restante de la Parcela: ", areaParcelaRestante, "m2")
    
    obtener_recomendacion_sector()
    # ************************************************** #
