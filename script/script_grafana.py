import time
import psutil
import mysql.connector
from datetime import datetime
from mysql.connector import Error
from conexion_sql import get_connection, close_connection
from datos_sistema import DatosSistema

def collect_data():
    """Recolecta los datos del sistema y los almacena en un objeto DatosSistema"""
    # Obtener detalles de los procesos
    proc_detail = [
        {
            "pid": proc.info["pid"],
            "name": proc.info["name"],
            "exe": proc.info["exe"] if proc.info["exe"] else "[{}]".format(proc.info["name"]),
            "status": proc.info["status"],
            "username": proc.info["username"] if proc.info["username"] else "N/A",
            "cpu_percent": proc.info["cpu_percent"],
            "memory_percent": proc.info["memory_percent"],
            "vsz": proc.memory_info().vms,
            "rss": proc.memory_info().rss,
            "num_thread": proc.num_threads()
        }
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'status', 'username', 'cpu_percent', 'memory_percent'])
        #if proc.info["status"] == "running"
    ]
    
    #Obtener el tiempo que el servidor ha estado activo
    boot_time = psutil.boot_time() #tiempo de arranque, momento en el que arrancó el servidor
    current_time = time.time()
    time_seconds = current_time - boot_time

    time_days = time_seconds // 86400
    time_hours = (time_seconds % 86400) // 3600
    time_minutes = (time_seconds % 3600) // 60
    time_seconds = time_seconds % 60
    
    data = DatosSistema(
        carga_cpu=psutil.cpu_percent(interval=1),
        frecuencia_cpu=psutil.cpu_freq().current,
        mem_ram=psutil.virtual_memory().percent,
        mem_swap=psutil.swap_memory().percent,
        espacio_disco=psutil.disk_usage('/').percent,
        io_operaciones=psutil.disk_io_counters().read_count,

        proc_detail=proc_detail,  # Lista detallada de procesos
        num_proc=len(proc_detail),  # Número de procesos en ejecución

        bytes_env=psutil.net_io_counters().bytes_sent,
        bytes_rec=psutil.net_io_counters().bytes_recv,
        conexiones=len(psutil.net_connections(kind='inet')),
        paq_env=psutil.net_io_counters().packets_sent,
        paq_rec=psutil.net_io_counters().packets_recv,

        dias=time_days,
        horas=time_hours,
        minutos=time_minutes,
        segundos=time_seconds
    )

    return data



def insert_data(data: DatosSistema, conn):
    """Inserta los datos en la base de datos usando el procedimiento almacenado"""
    if conn:
        try:
            cursor = conn.cursor()

            # Inicia una transacción
            conn.begin()

            #eliminar procesos anteriores
            cursor.execute("DELETE FROM procesos;")

            # Primero insertamos los procesos (procesos_en_ejecucion)
            cursor.executemany("""INSERT INTO procesos (pid, cpu_percent, memory_percent, vsz, rss, usuario, nombre, ruta, hilos, estado)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", data.to_tuple_proc_info()) #se realiza executemany para no hacer un bucle y ser más eficiente

            # Luego, llamamos al procedimiento almacenado
            cursor.callproc("AddDatos", data.to_tuple())

            # Confirmamos la transacción
            conn.commit()

            cursor.close()
            print("Datos insertados correctamente en la BD.")
        except Error as e:
            conn.rollback()  # Si algo falla, revertimos la transacción
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

            time.sleep(5)  # Espera 10 segundos antes de la siguiente medición
except Error as e:
    print(f"Error al conectar bas de datos: {e}")
finally:
    if conn:  # Si la conexión fue establecida, cierra la conexión
        close_connection(conn)  # Cerrar la conexión al finalizar el programa
