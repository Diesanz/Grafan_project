import os
import pymysql


def get_connection():
    try:
        """
        Establece una conexión con la base de datos MariaDB utilizando los parámetros proporcionados.
                
        return: Devuelve un objeto de tipo conexión a la base de datos si la conexión es exitosa.
                Si ocurre un error, devuelve None.
        """
        connection = pymysql.connect(
            host= "localhost",
            port= int(3306),
            database= "grafana",
            user= "grafanaReader",
            password= "Grupo6esi",
            charset='utf8mb4',  # Evita problemas de encoding
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print("Error al conectarse a la base de datos:" + str(e))
        return None

def close_connection(connection):
    """
    Cierra conexión con la base de datos

    parameters: 
        -connection: objetito de tipo conexión a base de datos la cual se quiere cerrar
    """
    if connection: 
        #si la conexión es válida se cierra conexión
        connection.close()