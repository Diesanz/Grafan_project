# Grafan_project

Proyecto de monitorización del sistema con Python, MariaDB/MySQL y Grafana.

Un script en Python recolecta métricas del sistema usando psutil y las inserta en una base de datos MariaDB/MySQL mediante un procedimiento almacenado. Grafana se usa como capa de visualización conectándose a esa base de datos para construir paneles y gráficos.


Contenido del repositorio
- db/ -> Scripts SQL para la base de datos (tablasGrafana.sql: tablas y procedimiento AddDatos)
- script/ -> Código Python
  - conexion_sql.py -> Conexión a MariaDB/MySQL
  - datos_sistema.py -> Clase contenedora de métricas y helpers de conversión a tuplas
  - script_grafana.py -> Recolección periódica (cada 5s) e inserción en BD
- latex/ -> Material del informe (LaTeX y recursos)
- README.md -> Este documento


Arquitectura y flujo
1) script_grafana.py usa psutil para recolectar métricas del sistema y construir un objeto DatosSistema.
2) Insertar en BD:
   - Tablas de estado "actual" se limpian e insertan de nuevo (cpu, disco, num_procesos, tiempo_activo, sistema) para mantener solo la última muestra.
   - La tabla procesos se vacía y se vuelve a poblar con los procesos actuales.
   - La tabla interfaces se vacía y se vuelve a poblar con el estado actual de las interfaces de red.
   - La tabla red inserta un registro por iteración (histórico).
3) Grafana se conecta a la base de datos (fuente de datos MySQL) y consulta estas tablas.


Prerrequisitos
- Sistema gestor de BD: MariaDB o MySQL 8+
- Python 3.9+ (recomendado 3.10 o superior)
- Grafana 9+
- Paquetes Python:
  - psutil
  - PyMySQL
  - mysql-connector-python (para compatibilidad con el manejo de excepciones importado en el script)


Instalación (Windows)
1) Crear y activar entorno virtual (opcional pero recomendado):
   - py -m venv venv
   - venv\Scripts\activate
2) Instalar dependencias:
   - pip install psutil PyMySQL mysql-connector-python
3) Configurar base de datos:
   - Iniciar MariaDB/MySQL
   - Crear base de datos y usuario (ajusta usuario/clave al gusto). En db/tablasGrafana.sql hay ejemplos comentados. Versión corregida del GRANT:
     - CREATE DATABASE grafana;
     - CREATE USER 'grafanareader'@'localhost' IDENTIFIED BY 'Grupo6esi';
     - GRANT ALL PRIVILEGES ON grafana.* TO 'grafanareader'@'localhost';
     - FLUSH PRIVILEGES;
   - Aplicar el script de tablas y procedimiento:
     - mysql -u root -p grafana < db/tablasGrafana.sql
4) Revisar credenciales de conexión en script/conexion_sql.py y ajustarlas a tu entorno (host, puerto, base de datos, usuario, contraseña).


Ejecución del recolector
- Con el entorno activado y la BD lista:
  - python script/script_grafana.py
- El script:
  - Se conecta a la BD.
  - Cada 5 segundos recolecta métricas e inserta en las tablas.
  - Muestra mensajes informativos en consola.
- Finalización limpia: al terminar, se cierra la conexión a la BD.


Esquema de tablas (resumen)
- cpu(timestamp PK, carga, frecuencia)
- memoria(timestamp PK, ram, swap)
- disco(timestamp PK, espacio)
- entradasalida(timestamp PK, operaciones)
- num_procesos(timestamp PK, numero)
- procesos(timestamp, pid, cpu_percent, memory_percent, vsz, rss, usuario, nombre, ruta, hilos, estado)
- red(timestamp PK, bytes_enviados, bytes_recibidos, conexiones_activas, paquetes_enviados, paquetes_recibidos)
- interfaces(timestamp, nombre, direccion, mascara, mac, broadcast, bytes_enviados, bytes_recibidos)
- tiempo_activo(timestamp PK, dias, horas, minutos, segundos)
- sistema(timestamp PK, carga1, carga5, carga15, nucleos_log)

Nota: El procedimiento almacenado AddDatos hace DELETE de varias tablas antes de insertar para mantener el último estado. Si deseas histórico completo, elimina esos DELETE del procedimiento.


Conectar Grafana (Data Source MySQL)
- Tipo: MySQL
- Host: localhost:3306
- Database: grafana
- User: grafanareader
- Password: la configurada
- Cambios recomendados:
  - Min time interval: 5s (coincidiendo con la frecuencia del script)
  - Timezone: según preferencia


Consultas de ejemplo para paneles en Grafana
- CPU (gauge):
  - SELECT carga FROM cpu ORDER BY timestamp DESC LIMIT 1;
- Frecuencia CPU (stat):
  - SELECT frecuencia FROM cpu ORDER BY timestamp DESC LIMIT 1;
- Memoria (gauge):
  - SELECT ram FROM memoria ORDER BY timestamp DESC LIMIT 1;
- Carga del sistema (time series):
  - SELECT timestamp, carga1, carga5, carga15 FROM sistema ORDER BY timestamp;
- Disco (gauge):
  - SELECT espacio FROM disco ORDER BY timestamp DESC LIMIT 1;
- E/S disco (time series):
  - SELECT timestamp, operaciones FROM entradasalida ORDER BY timestamp;
- Red (time series):
  - SELECT timestamp, bytes_enviados, bytes_recibidos, conexiones_activas, paquetes_enviados, paquetes_recibidos FROM red ORDER BY timestamp;
- Top procesos por CPU (table):
  - SELECT nombre, cpu_percent, memory_percent, hilos, estado FROM procesos ORDER BY cpu_percent DESC LIMIT 10;
- Interfaces (table):
  - SELECT nombre, direccion, mascara, mac, broadcast, bytes_enviados, bytes_recibidos FROM interfaces ORDER BY nombre;
- Tiempo activo (stat):
  - SELECT (dias*86400 + horas*3600 + minutos*60 + segundos) AS uptime_seg FROM tiempo_activo ORDER BY timestamp DESC LIMIT 1;


Notas sobre el código
- script/conexion_sql.py usa PyMySQL para conectarse. Ajusta los parámetros a tu entorno.
- script/script_grafana.py importa mysql.connector.Error para manejo de excepciones; por eso se incluye mysql-connector-python como dependencia.
- datos_sistema.py define la clase DatosSistema y helpers:
  - to_tuple(): datos principales para el procedimiento AddDatos
  - to_tuple_proc_info(): lista de tuplas para insertar procesos con executemany
  - to_tuple_interfaces_detail(): lista de tuplas para insertar interfaces con executemany


Latex (opcional)
- latex/Práctica1_ Grafana/main.tex contiene un informe con figuras de ejemplo. Para compilar:
  - Usar TeX Live o MiKTeX
  - pdflatex -> biber (si usa bibliografía) -> pdflatex -> pdflatex


Solución de problemas comunes
- Access denied al conectar a la BD:
  - Verificar usuario/clave y privilegios (GRANT ALL PRIVILEGES ON grafana.* TO 'grafanareader'@'localhost').
- Tablas o procedimiento no existen:
  - Asegúrate de haber ejecutado db/tablasGrafana.sql contra la base de datos grafana.
- psutil falla por permisos:
  - Ejecuta el intérprete con permisos suficientes.
- No ves datos en Grafana:
  - Verifica que el script esté corriendo y que las consultas usen la base de datos correcta.
  - Alinea el rango de tiempo del dashboard con la actividad reciente (Last 15 minutes, etc.).


Licencia
- No se ha definido una licencia explícita en el repositorio.
