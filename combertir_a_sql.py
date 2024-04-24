from conf import *
import pandas as pd

df_datos = pd.read_csv(path.join(CARPETA_DATOS_CSV,FICHERO_DATOS_DATOS))

# Nombre del archivo SQL que vamos a crear
nombre_archivo_sql = "datos_insert.sql"

with open(nombre_archivo_sql, 'w') as file:
    # Escribir el comando para usar la base de datos
    file.write("USE muundoGando;\n")

    # Comenzar la declaración INSERT INTO
    file.write("INSERT INTO gps (Numero_pendiente, IdUsuario, latitude, longitude, fecha, id_parcela,tipo,velocidad,anomalia,fuera_del_recinto) VALUES\n")

    # Recorrer cada fila del DataFrame y añadir a la declaración SQL
    for index, row in df_datos.iterrows():
        file.write(f"""({int(row['Numero_pendiente'])},
{1},
{row['latitude']},
{row['longitude']},
{int(row['id_parcela'])}),
{(row['tipo'])}),
{float(row['velocidad'])}),
{bool(row['anomalia'])}),
{bool(row['fuera_del_recinto'])}),
'{row['fecha']},'
            \n""")

    # Volver al archivo y remover la última coma
    file.seek(0, 2)                 # Mover al final del archivo
    file.seek(file.tell() - 2, 0)   # Retroceder dos caracteres (',' y '\n')
    file.truncate()                 # Truncar el archivo aquí

    # Terminar la instrucción SQL
    file.write(";\n")