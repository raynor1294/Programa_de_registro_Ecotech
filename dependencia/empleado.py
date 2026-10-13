import uuid

class Empleado:
    def __init__(self, nombre: str, email: str):
        self.id_empleado = str(uuid.uuid4())[:8]  # ID único automático de 8 caracteres
        self.nombre = nombre
        self.email = email

    def calcular_pago(self) -> float:
        raise NotImplementedError("Método abstracto, debe ser implementado por subclases.")

    def mostrar_datos(self) -> str:
        return f"ID: {self.id_empleado} | {self.nombre} ({self.email})"

class EmpleadoMensual(Empleado):
    def __init__(self, nombre: str, email: str, salario_mensual: float):
        super().__init__(nombre, email)
        self.salario_mensual = salario_mensual

    def calcular_pago(self) -> float:
        return self.salario_mensual

    def mostrar_datos(self) -> str:
        return f"{super().mostrar_datos()} | Tipo: Mensual | Pago: ${self.calcular_pago():,}"

class EmpleadoPorHora(Empleado):
    def __init__(self, nombre: str, email: str, valor_hora: float):
        super().__init__(nombre, email)
        self.valor_hora = valor_hora
        self.horas_trabajadas = 0.0

    def registrar_horas(self, horas: float):
        if horas > 0:
            self.horas_trabajadas += horas

    def calcular_pago(self) -> float:
        return self.horas_trabajadas * self.valor_hora

    def mostrar_datos(self) -> str:
        return f"{super().mostrar_datos()} | Tipo: Por Hora | Horas: {self.horas_trabajadas} | Pago: ${self.calcular_pago():,}"