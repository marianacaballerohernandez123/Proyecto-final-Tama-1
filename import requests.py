import requests
import pandas as pd
import sqlite3

# URL del archivo CSV
url = "https://www.datos.gov.co/resource/kjrc-gte7.csv?$limit=100000000"

# Nombre del archivo temporal
temp_csv = "datos_descargados.csv"

# 1. Descargar el archivo CSV
print("Descargando datos...")
response = requests.get(url)
if response.status_code == 200:
    with open(temp_csv, "wb") as file:
        file.write(response.content)
    print(f"Archivo descargado y guardado como: {temp_csv}")
else:
    print(f"Error al descargar el archivo: {response.status_code}")
    exit()

# 2. Cargar el archivo CSV en un DataFrame
print("Cargando datos en un DataFrame...")
dataset = pd.read_csv(temp_csv)

# 3. Conectar a la base de datos SQLite
database = "mi_base_datos.db"
connection = sqlite3.connect(database)
print(f"Conectado a la base de datos: {database}")

# 4. Almacenar los datos en SQLite
tabla = "datos_tabla"
print(f"Guardando datos en la tabla '{tabla}'...")
dataset.to_sql(tabla, connection, if_exists="replace", index=False)
print(f"Datos guardados correctamente en la tabla '{tabla}'.")

# 5. Verificar los datos
print("Verificando los datos almacenados...")
cursor = connection.cursor()
cursor.execute(f"SELECT * FROM {tabla} LIMIT 5;")
for row in cursor.fetchall():
    print(row)

# 6. Cerrar la conexión
connection.close()
print("Conexión cerrada.")

import sqlite3

# Conexión a la base de datos SQLite
database = "mi_base_datos.db"
connection = sqlite3.connect(database)
cursor = connection.cursor()

# Crear la tabla municipios
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS municipios (
    codigo_dane INTEGER PRIMARY KEY,
    municipio TEXT NOT NULL
);
"""
)

# Crear la tabla incidentes
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS incidentes (
    id_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_dane INTEGER,
    armas_medios TEXT,
    fecha_hecho DATE,
    genero TEXT,
    grupo_etario TEXT,
    cantidad INTEGER,
    FOREIGN KEY (codigo_dane) REFERENCES municipios (codigo_dane)
);
"""
)

# Confirmar cambios
connection.commit()

print("Tablas creadas exitosamente.")

# Cerrar la conexión
connection.close()
import sqlite3

# Conectar a la base de datos
database = "mi_base_datos.db"
connection = sqlite3.connect(database)
cursor = connection.cursor()

# Listar todas las tablas
print("Listando tablas disponibles:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
for tabla in tablas:
    print(f"- {tabla[0]}")

# Consultar estructura de la tabla municipios
print("\nEstructura de la tabla 'municipios':")
cursor.execute("PRAGMA table_info(municipios);")
for column in cursor.fetchall():
    print(column)

# Consultar estructura de la tabla incidentes
print("\nEstructura de la tabla 'incidentes':")
cursor.execute("PRAGMA table_info(incidentes);")
for column in cursor.fetchall():
    print(column)

# Cerrar la conexión
connection.close()
