from datetime import datetime, timedelta
from os import path, mkdir
# Función para generar una fecha aleatoria dentro del último año
fecha_inicial = datetime.now() - timedelta(days=30)

VERBOSE = True

PORCENTAJE_DE_TIEMPO_CAMINANDO = 0.2
SIGMA_CAMINANDO = 0.00005 # El nivel de movimiento que tiene una vaca, usa la funcion normal para obtener el siguiente punto
VELOCIDAD_CAMINANDO = 1/2


PORCENTAJE_DE_TIEMPO_PASTANDO = 0.4
SIGMA_PASTANDO = 0.005 # El nivel de movimiento que tiene una vaca, usa la funcion normal para obtener el siguiente punto
VELOCIDAD_PASTANDO = 1/25

PORCENTAJE_DE_TIEMPO_DESCANSANDO = 1 - PORCENTAJE_DE_TIEMPO_CAMINANDO -PORCENTAJE_DE_TIEMPO_PASTANDO
SIGMA_DESCANSANDO = 0.005 # El nivel de movimiento que tiene una vaca, usa la funcion normal para obtener el siguiente punto
VELOCIDAD_DESCANSANDO = 1/50


MINUTOS = 2 # El tiempo que se tarda en obtener un dato y otro
RANGO = 1000 # El numero de puntos por vaca y por parcela
PROBABILIDAD_ANOMALIA = 0.001 # Probabilidad con la que una vaca va a tener una anomalia
SIGMA_ANOMALIA = 0.0001 # El nivel de movimiento de la anomalia
NUMERO_DE_VACAS = 10 # Número de vacas que se van a crear
NUMERO_PARCELAS = 1 # Número de parcelas a crear
PARA_SQL =  True # Si se quiere guardar en un fichero para pasarlo a sql.
# Aquí vamos a definir las esquinas de las parcelas.

CARPETA_DATOS_CSV = 'datos_csv'

if (not path.exists(CARPETA_DATOS_CSV)):
    mkdir = CARPETA_DATOS_CSV

FICHERO_DATOS_PARCELA = 'parcelas.csv'
FICHERO_DATOS_ENFERMEDADES = 'enfermedades.csv'
FICHERO_DATOS_PARTOS = 'partos.csv'
FICHERO_DATOS_VACAS = 'vacas.csv'
FICHERO_DATOS_DATOS = 'datos.csv'
FICHERO_DATOS_DATOS_PROCESADOS = 'datos_procesados.csv'
FICHERO_DATOS_ANOMALIAS = 'anomalias.csv'

parcelas = None

parcelas = [
    [
        (42.1708749220415 ,  -8.684778213500977),
        (42.17088784344455 ,  -8.683796525001526),
        (42.171329902931646 ,  -8.683318421244621),
        (42.171783638124204 ,   -8.68295531719923),
        (42.17215164330223 ,  -8.682750463485718),
        (42.17232210277389 ,  -8.683327473700047),
        (42.17273135272034 ,  -8.684871755540371),
        (42.17178438357912 ,   -8.68525430560112)
    ]
]
PONER_ANOMALIAS = False