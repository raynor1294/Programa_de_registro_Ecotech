from dependencia.empleado import Empleado

class Proyecto:
    def __init__(self, nombre: str, descripcion: str):
        self.nombre = nombre
        self.descripcion = descripcion 
        self._equipo = []               # Lista privada encapsulada

    @property
    def equipo(self) -> tuple:
        return tuple(self._equipo)

    def asignar_empleado(self, emp: Empleado) -> bool:
        if emp in self._equipo:
            return False
        self._equipo.append(emp)
        return True