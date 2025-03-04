import time
import psutil
import mysql.connector
from datetime import datetime
from mysql.connector import Error
from conexion_sql import get_connection, close_connection
from datos_sistema import DatosSistema

def collect_data():
    """Recolecta los datos del sistema y los almacena en un objeto DatosSistema"""
    data = DatosSistema(
        carga_cpu=psutil.cpu_percent(interval=1),
        frecuencia_cpu=psutil.cpu_freq().current,
        mem_ram=psutil.virtual_memory().percent,
        mem_swap=psutil.swap_memory().percent,
        espacio_disco=psutil.disk_usage('/').percent,
        io_operaciones=psutil.disk_io_counters().read_count,
        proc_id=0,  # ID de proceso no aplicable en este contexto
        proc_activo=0,  # No es relevante aquí
        bytes_env=psutil.net_io_counters().bytes_sent,
        bytes_rec=psutil.net_io_counters().bytes_recv,
        conexiones=len(psutil.net_connections(kind='inet'))
    )

    return data

def insert_data(data: DatosSistema, conn):
    
    """Inserta los datos en la base de datos usando el procedimiento almacenado"""
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc("AddDatos", data.to_tuple()) 
            conn.commit()
            cursor.close()
            print("Datos insertados correctamente en la BD.")
        except Error as e:
            print(f"Error al insertar datos: {e}")


conn = None

try:
    
    conn = get_connection()

    if conn:
        print("Conexión a la base de datos establecida correctamente")

        """Ejecuta la recolección de datos e inserción en la BD en intervalos regulares"""
        while True:
            data = collect_data()
            if data:
                insert_data(data, conn)

            time.sleep(10)  # Espera 10 segundos antes de la siguiente medición
except Error as e:
    print(f"Error al conectar bas de datos: {e}")
finally:
    if conn:  # Si la conexión fue establecida, cierra la conexión
        close_connection(conn)  # Cerrar la conexión al finalizar el programa

