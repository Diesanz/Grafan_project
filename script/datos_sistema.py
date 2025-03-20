class DatosSistema:
    def __init__(self, carga_cpu, frecuencia_cpu, mem_ram, mem_swap,
                 espacio_disco, io_operaciones, proc_detail, num_proc,
                 bytes_env, bytes_rec, conexiones, paq_env, paq_rec, dias, horas, minutos, segundos,interfaces_detail):
        """
        Constructor de la clase `DatosSistema`. Inicializa todos los atributos con los valores recibidos.
        
        parameters:
        - carga_cpu: Porcentaje de uso de la CPU.
        - frecuencia_cpu: Frecuencia actual de la CPU (en MHz).
        - mem_ram: Porcentaje de memoria RAM utilizada.
        - mem_swap: Porcentaje de memoria swap utilizada.
        - espacio_disco: Porcentaje de espacio en disco utilizado.
        - io_operaciones: Número de operaciones de entrada/salida en disco.
        - proc_detail: Lista de detalles de los procesos en ejecución.
        - num_proc: Número total de procesos en ejecución.
        - bytes_env: Bytes enviados por la red.
        - bytes_rec: Bytes recibidos por la red.
        - conexiones: Número de conexiones de red activas.
        - paq_env: Número de paquetes enviados por la red.
        - paq_rec: Número de paquetes recibidos por la red.
        - dias: Días desde el arranque del sistema.
        - horas: Horas desde el arranque del sistema.
        - minutos: Minutos desde el arranque del sistema.
        - segundos: Segundos desde el arranque del sistema.
        - interfaces_detail: Lista de detalles de lso procesos en ejecución
        
        return:
        - Inicializa los atributos de la instancia con los valores proporcionados.
        """
        self.carga_cpu = carga_cpu
        self.frecuencia_cpu = frecuencia_cpu
        self.mem_ram = mem_ram
        self.mem_swap = mem_swap
        self.espacio_disco = espacio_disco
        self.io_operaciones = io_operaciones
        self.num_proc = num_proc

        self.proc_info = proc_detail  # Lista de detalles de los procesos

        self.bytes_env = bytes_env
        self.bytes_rec = bytes_rec
        self.conexiones = conexiones
        self.paq_env = paq_env
        self.paq_rec = paq_rec

        self.dias = dias
        self.horas = horas
        self.minutos = minutos
        self.segundos = segundos
        self.interfaces_detail = interfaces_detail

    def to_tuple(self):
        """
        Convierte los datos del sistema en una tupla para ser insertada de una forma más facil en la base de datos.
        
        parameters: No recibe parámetros.
        
        return: Devuelve una tupla con los datos del sistema:
            (carga_cpu, frecuencia_cpu, mem_ram, mem_swap, espacio_disco,
             io_operaciones, num_proc, bytes_env, bytes_rec, conexiones,
             paq_env, paq_rec, dias, horas, minutos, segundos)
        """
        return (self.carga_cpu, self.frecuencia_cpu, self.mem_ram, self.mem_swap,
                self.espacio_disco, self.io_operaciones, self.num_proc,
                self.bytes_env, self.bytes_rec, self.conexiones, self.paq_env, self.paq_rec, self.dias, self.horas, self.minutos, self.segundos)

    def to_tuple_proc_info(self):
        """
        Convierte los detalles de los procesos en una lista de tuplas para ser insertada en la base de datos.
        
        parameters: No recibe parámetros.
        
        return: Devuelve una LISTA de tuplas, donde cada tupla contiene los detalles de un proceso:
            (pid, cpu_percent, memory_percent, vsz, rss, usuario, nombre, ruta, hilos, estado)
        """
        return [(proc["pid"], proc["cpu_percent"], proc["memory_percent"], proc["vsz"], proc["rss"],
                 proc["username"], proc["name"], proc["exe"], proc["num_thread"], proc["status"]) for proc in self.proc_info]
    
    def to_tuple_interfaces_detail(self):
        """
        Convierte los detalles de las interfaces de red en una lista de tuplas para ser insertada en la base de datos.
        
        parameters: No recibe parámetros.
        
        return: Devuelve una LISTA de tuplas, donde cada tupla contiene los detalles de una interfaz:
            (nombre, direccion, mascara, mac, broadcast)
        """
        return [(interfaz["nombre"], interfaz["direccion"], interfaz["mascara"], interfaz["mac"],
                  interfaz["broadcast"]) for interfaz in self.interfaces_detail]
