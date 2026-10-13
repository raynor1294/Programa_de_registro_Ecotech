from dependencia.empleado import Empleado
from dependencia.proyecto import Proyecto

class RegistroTrabajo:
    """Clase intermedia que materializa la relación con información propia de EcoTech"""
    def __init__(self, fecha: str, horas: float, descripcion: str, empleado: Empleado, proyecto: Proyecto):
        self.id_registro = None  # Se asignará al guardar en la Base de Datos
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion
        self.empleado = empleado
        self.proyecto = proyecto

    def obtener_resumen(self) -> str:
        return f"Fecha: {self.fecha} | {self.empleado.nombre} trabajó {self.horas} hrs en '{self.proyecto.nombre}' -> {self.descripcion}"