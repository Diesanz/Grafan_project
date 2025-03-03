
class DatosSistema():
    def __init__(self, carga_cpu, frecuencia_cpu, mem_ram, mem_swap, 
                 espacio_disco, io_operaciones, proc_id, proc_activo, 
                 bytes_env, bytes_rec, conexiones):
        self.carga_cpu = carga_cpu
        self.frecuencia_cpu = frecuencia_cpu
        self.mem_ram = mem_ram
        self.mem_swap = mem_swap
        self.espacio_disco = espacio_disco
        self.io_operaciones = io_operaciones
        self.proc_id = proc_id
        self.proc_activo = proc_activo
        self.bytes_env = bytes_env
        self.bytes_rec = bytes_rec
        self.conexiones = conexiones
    
    def to_tuple(self):
        return (self.carga_cpu, self.frecuencia_cpu, self.mem_ram, self.mem_swap, 
                self.espacio_disco, self.io_operaciones, self.proc_id, self.proc_activo, 
                self.bytes_env, self.bytes_rec, self.conexiones)