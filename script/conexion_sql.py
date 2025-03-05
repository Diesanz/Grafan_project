import os
import pymysql


def get_connection():
    try:
        # Obtén los secretos desde variables de entorno
        host = "localhost"
        port = int(3306)
        database = "grafana"
        user = "grafanareader"
        password = "Grupo6esi"

        # Conéctate a MariaDB
        connection = pymysql.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            charset='utf8mb4',  # Evita problemas de encoding
            cursorclass=pymysql.cursors.DictCursor
        )
       # print("✅ Conexión a la base de datos establecida correctamente")
        return connection
    except pymysql.MySQLError as e:
        print(f"❌ Error al conectarse a la base de datos: {e}")
        return None

def close_connection(connection):
    if connection:
        connection.close()
       # print("🔒 Conexión cerrada correctamente")