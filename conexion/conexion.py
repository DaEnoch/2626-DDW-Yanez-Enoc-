# conexion/conexion.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# en Render se usa la variable de entorno DATABASE_URL
# en local se usa la base musica_db de tu PostgreSQL
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/musica_db'
)


def get_connection():
    # abre una conexion nueva a PostgreSQL
    return psycopg2.connect(DATABASE_URL)


def get_cursor(conn):
    # cursor que devuelve cada fila como diccionario
    return conn.cursor(cursor_factory=RealDictCursor)


def inicializar_bd():
    # ejecuta sql/esquema.sql para crear las tablas si no existen
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(base, 'sql', 'esquema.sql')

    with open(ruta, encoding='utf-8') as archivo:
        script = archivo.read()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(script)
    conn.commit()
    cursor.close()
    conn.close()
