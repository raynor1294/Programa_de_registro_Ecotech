from dependencia.empleado import Empleado

class Departamento:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._empleados = []       # Estado encapsulado (lista privada)
        self.gerente = None        # Asociación de rol (puede iniciar vacía)

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)  # Entrega una vista inmutable (Evita manipulación externa)

    def cantidad_empleados(self) -> int:
        return len(self._empleados)

    def asignar_gerente(self, emp: Empleado):
        self.gerente = emp

    def agregar_empleado(self, emp: Empleado) -> bool:
        # Validación del dominio: evita duplicar la misma instancia en memoria
        if emp in self._empleados:
            return False
        self._empleados.append(emp)
        return True