import time
import psutil
import mysql.connector

from datetime import datetime
from mysql.connector import Error
from conexion_sql import get_connection, close_connection
from datos_sistema import DatosSistema

def interfaces_values():
    """
    Obtiene información detallada sobre las interfaces de red del sistema.

    return:
        - list: Lista de diccionarios con la información de cada interfaz de red, 
          donde cada diccionario contiene los siguientes campos:

            - nombre (str): Nombre de la interfaz de red.
            - direccion (str | None): Dirección IPv4 asignada a la interfaz (o `None` si no tiene).
            - mascara (str | None): Máscara de subred de la interfaz (o `None` si no tiene).
            - mac (str | None): Dirección MAC de la interfaz (o `None` si no tiene).
            - broadcast (str | None): Dirección de broadcast de la interfaz (o `None` si no tiene).
            - bytes_enviados (int): Número total de bytes enviados a través de la interfaz.
            - bytes_recibidos (int): Número total de bytes recibidos a través de la interfaz.
    """
    
    interfaces_info = []
    for nombre_interfaz, interface_addreses in psutil.net_if_addrs().items():
            direccion_mac = None
            direccion_ipv4 = None
            subnet = None
            broadcast = None
            net_io = psutil.net_io_counters(pernic=True)

            for address in interface_addreses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    direccion_ipv4 = address.address if address.address else "IPv4"
                    subnet = address.netmask if address.netmask else "N/A"
                    broadcast = address.broadcast if address.broadcast else "N/A"
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    direccion_mac = address.address if address.address else "MAC"

            bytes_enviados = net_io[nombre_interfaz].bytes_sent if nombre_interfaz in net_io else 0
            bytes_recibidos = net_io[nombre_interfaz].bytes_recv if nombre_interfaz in net_io else 0

            if direccion_ipv4 or direccion_mac:
                interfaces_info.append({
                    "nombre": nombre_interfaz,
                    "direccion": direccion_ipv4,
                    "mascara": subnet,
                    "mac": direccion_mac,
                    "broadcast": broadcast,
                    "bytes_enviados" : bytes_enviados,
                    "bytes_recibidos" : bytes_recibidos
                })

    return interfaces_info

def collect_data(boot_time):
    """
    Recolecta los datos del sistema y los almacena en un objeto `DatosSistema`.

    parameters:
        - boot_time (float): Tiempo de arranque del sistema en segundos.

    return:
        - DatosSistema: Objeto con los siguientes atributos:
        
            - carga_cpu (float): Porcentaje de carga de la CPU.
            - frecuencia_cpu (float): Frecuencia actual de la CPU en MHz.
            - mem_ram (float): Porcentaje de uso de la memoria RAM.
            - mem_swap (float): Porcentaje de uso de la memoria swap.
            - espacio_disco (float): Porcentaje de uso del disco en la raíz (`/`).
            - io_operaciones (int): Número de operaciones de lectura en disco.
            - proc_detail (list): Lista de diccionarios con detalles de los procesos en ejecución, 
              incluyendo:
                - pid (int): Identificador del proceso.
                - name (str): Nombre del proceso.
                - exe (str): Ruta del ejecutable del proceso.
                - status (str): Estado actual del proceso.
                - username (str): Usuario propietario del proceso.
                - cpu_percent (float): Porcentaje de uso de CPU del proceso.
                - memory_percent (float): Porcentaje de uso de memoria del proceso.
                - vsz (int): Tamaño virtual del proceso en bytes.
                - rss (int): Tamaño de la memoria residente del proceso en bytes.
                - num_thread (int): Número de hilos del proceso.
            - num_proc (int): Número total de procesos en ejecución.
            - bytes_env (int): Cantidad de bytes enviados por la red.
            - bytes_rec (int): Cantidad de bytes recibidos por la red.
            - conexiones (int): Número de conexiones de red activas.
            - paq_env (int): Número de paquetes enviados por la red.
            - paq_rec (int): Número de paquetes recibidos por la red.
            - interfaces_detail (dict): Información detallada de las interfaces de red.
            - dias (int): Días transcurridos desde el arranque del sistema.
            - horas (int): Horas transcurridas desde el arranque del sistema.
            - minutos (int): Minutos transcurridos desde el arranque del sistema.
            - segundos (int): Segundos transcurridos desde el arranque del sistema.
            - carga_sis_1 (float): Carga promedio del sistema en el último minuto.
            - carga_sis_5 (float): Carga promedio del sistema en los últimos 5 minutos.
            - carga_sis_15 (float): Carga promedio del sistema en los últimos 15 minutos.
            - nucleos_log (int): Número de núcleos lógicos de la CPU.
    """

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
    ]

    #Obtener detalles de las interfaces
    interfaces_detail = interfaces_values()

    current_time = time.time()
    time_seconds = current_time - boot_time

    # Calcular el tiempo en días, horas, minutos y segundos
    time_days = time_seconds // 86400
    time_hours = (time_seconds % 86400) // 3600
    time_minutes = (time_seconds % 3600) // 60
    time_seconds = time_seconds % 60

    # Crear el objeto DatosSistema con los datos recolectados
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
        segundos=time_seconds,
        interfaces_detail = interfaces_detail,
        carga_sis_1=psutil.getloadavg()[0],
        carga_sis_5=psutil.getloadavg()[1],
        carga_sis_15=psutil.getloadavg()[2],
        nucleos_log = psutil.cpu_count(logical=False)
    )

    return data  # Devuelve el objeto `DatosSistema` con todos los datos del sistema

def insert_data(data: DatosSistema, conn):
    """
    Inserta los datos recolectados en la base de datos utilizando un procedimiento almacenado.

    parameters:
    - `data`: Un objeto `DatosSistema` que contiene los datos recolectados del sistema.
    - `conn`: Conexión a la base de datos MySQL.

    return: No devuelve nada. Inserta los datos en la base de datos.
    """
    if conn:
        try:
            cursor = conn.cursor()

            # Inicia una transacción
            conn.begin()

            # Eliminar procesos anteriores
            cursor.execute("DELETE FROM procesos;")

            # Insertar los detalles de los procesos
            #Esto se realiza debido a que hay que insertar varios procesos en la tabla
            cursor.executemany("""INSERT INTO procesos (pid, cpu_percent, memory_percent, vsz, rss, usuario, nombre, ruta, hilos, estado)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", data.to_tuple_proc_info())  # `data.to_tuple_proc_info()` devuelve los detalles de los procesos

            # Borrar los detalles anteriores de las interfaces
            cursor.execute("DELETE FROM interfaces;")

            # Insertar los detalles de las interfaces de red.
            cursor.executemany("""INSERT INTO interfaces (nombre, direccion, mascara, mac, broadcast, bytes_enviados, bytes_recibidos)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)""", data.to_tuple_interfaces_detail())

            # Llamar al procedimiento almacenado para insertar los otros datos del sistema
            cursor.callproc("AddDatos", data.to_tuple())  # `data.to_tuple()` devuelve los otros datos en formato adecuado para el procedimiento

            # Confirmar la transacción
            conn.commit()

            cursor.close()
            print("Datos insertados correctamente en la BD.")
        except Error as e:
            conn.rollback()  # Si ocurre un error, revertir la transacción
            print(f"Error al insertar datos: {e}")

# Configuración de conexión a la base de datos
conn = None

try:
    conn = get_connection()  # Obtener la conexión a la base de datos

    if conn:
        print("Conexión a la base de datos establecida correctamente")
        # Obtener el tiempo que el servidor ha estado activo
        boot_time = psutil.boot_time()  # Tiempo de arranque, momento en el que arrancó el servidor

        # Ejecuta la recolección e inserción de datos en intervalos regulares
        while True:
            data = collect_data(boot_time)  # Llama a la función collect_data para recolectar los datos
            if data:
                insert_data(data, conn)  # Llama a la función insert_data para insertar los datos en la base de datos

            time.sleep(5)  # Espera 5 segundos antes de la siguiente medición
except Error as e:
    print("Error al conectar con la base de datos:" + str(e))
finally:
    if conn:  # Si la conexión fue exitosa, se cierra
        close_connection(conn)  # Cierra la conexión al finalizar el programa
