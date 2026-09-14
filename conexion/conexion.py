# conexion/conexion.py
import mysql.connector

# datos de conexion a la base de datos local
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'musica_db'
}


def get_connection():
    # abre y devuelve una conexion nueva a MySQL
    return mysql.connector.connect(**DB_CONFIG)
