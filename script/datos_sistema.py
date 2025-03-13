class DatosSistema():
    def __init__(self, carga_cpu, frecuencia_cpu, mem_ram, mem_swap,
                 espacio_disco, io_operaciones, proc_detail, num_proc,
                 bytes_env, bytes_rec, conexiones, paq_env, paq_rec, dias, horas, minutos, segundos):
        self.carga_cpu = carga_cpu
        self.frecuencia_cpu = frecuencia_cpu
        self.mem_ram = mem_ram
        self.mem_swap = mem_swap
        self.espacio_disco = espacio_disco
        self.io_operaciones = io_operaciones
        self.num_proc = num_proc

        self.proc_info = proc_detail

        self.bytes_env = bytes_env
        self.bytes_rec = bytes_rec
        self.conexiones = conexiones
        self.paq_env = paq_env
        self.paq_rec = paq_rec

        self.dias = dias
        self.horas = horas
        self.minutos = minutos
        self.segundos = segundos

    def to_tuple(self):
        return (self.carga_cpu, self.frecuencia_cpu, self.mem_ram, self.mem_swap,
                self.espacio_disco, self.io_operaciones, self.num_proc,
                self.bytes_env, self.bytes_rec, self.conexiones, self.paq_env, self.paq_rec, self.dias, self.horas, self.minutos, self.segundos)

    def to_tuple_proc_info(self):
        return [(proc["pid"], proc["cpu_percent"], proc["memory_percent"], proc["vsz"], proc["rss"],
                proc["username"], proc["name"], proc["exe"], proc["num_thread"], proc["status"]) for proc in self.proc_info] #devuelve una lista de tuplas
