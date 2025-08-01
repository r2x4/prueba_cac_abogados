import pandas as pd
import urllib
from sqlalchemy import create_engine
import os

# Parámetros
server = 'DESKTOP-BUAC79Q\\SQLEXPRESS01'  # Nombre del servidor
database = 'PRACTICA'                    # Nombre de la base de datos
archivo_datos = 'datos1.csv'            # Nombre del archivo CSV
nombre_tabla = 'datos1'                 # Nombre de la tabla a crear

try:
    # Verificar que el archivo CSV existe
    if not os.path.exists(archivo_datos):
        raise FileNotFoundError(f"Archivo no encontrado: {archivo_datos}")

    # Leer el archivo CSV (probar UTF-8 o Latin1 si falla)
    try:
        df = pd.read_csv(archivo_datos, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(archivo_datos, encoding='latin1')

    print("✅ CSV leído correctamente. Primeras filas:")
    print(df.head())

    # Crear cadena de conexión con autenticación de Windows
    connection_string = urllib.parse.quote_plus(
        f"DRIVER=ODBC Driver 17 for SQL Server;"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")

    # Subir el DataFrame a SQL Server
    df.to_sql(nombre_tabla, con=engine, if_exists='replace', index=False)
    print(f"✅ Datos subidos exitosamente a la tabla '{nombre_tabla}' en la base de datos '{database}'.")

except Exception as e:
    print("❌ Error durante la operación:")
    print(e)




