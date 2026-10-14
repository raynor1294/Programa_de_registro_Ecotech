from dependencia.empleado import Empleado, EmpleadoMensual, EmpleadoPorHora
from persistencia.conexion import abrir_conexion, marcador_sql

class EmpleadoDAO:
    
    @staticmethod
    def _fila_a_empleado(fila: tuple) -> Empleado:
        if not fila:
            return None
        id_emp, nombre, email, tipo, metrica_pago = fila
        
        if tipo == "Mensual":
            emp = EmpleadoMensual(nombre, email, salario_mensual=float(metrica_pago))
        else:
            emp = EmpleadoPorHora(nombre, email, valor_hora=float(metrica_pago))
            
        emp.id_empleado = id_emp
        return emp

    @staticmethod
    def insertar(empleado: Empleado) -> bool:
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            tipo = "Mensual" if isinstance(empleado, EmpleadoMensual) else "PorHora"
            metrica = empleado.salario_mensual if tipo == "Mensual" else empleado.valor_hora
            
            sql = f"INSERT INTO empleado (id, nombre, correo, tipo, metrica_pago) VALUES ({marca}, {marca}, {marca}, {marca}, {marca})"
            cursor.execute(sql, (empleado.id_empleado, empleado.nombre, empleado.email, tipo, metrica))
            conexion.commit()  # Confirma la transacción segura
            return True
        except Exception:
            if conexion:
                conexion.rollback()  # Revierte los cambios ante fallas parciales
            raise
        finally:
            if conexion:
                conexion.close()  # Cierre seguro garantizado de la conexión

    @staticmethod
    def buscar_por_id(id_empleado: str) -> Empleado:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()
        
        sql = f"SELECT id, nombre, correo, tipo, metrica_pago FROM empleado WHERE id = {marca}"
        cursor.execute(sql, (id_empleado,))
        fila = cursor.fetchone()
        
        if not fila:
            conexion.close()
            return None
            
        id_emp, nombre, email, tipo, metrica_pago = fila
        
        if tipo == "PorHora":
            sql_horas = f"SELECT SUM(horas) FROM registro_trabajo WHERE empleado_id = {marca}"
            cursor.execute(sql_horas, (id_empleado,))
            fila_horas = cursor.fetchone()
            horas_totales = fila_horas[0] if fila_horas[0] is not None else 0.0
            
            emp = EmpleadoPorHora(nombre, email, valor_hora=float(metrica_pago))
            emp.id_empleado = id_emp
            emp.registrar_horas(horas_totales) 
        else:
            # Si es mensual, mantiene su flujo normal de salario fijo
            emp = EmpleadoMensual(nombre, email, salario_mensual=float(metrica_pago))
            emp.id_empleado = id_emp
            
        conexion.close()
        return emp
    @staticmethod
    def buscar_por_correo(correo: str) -> Empleado:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()
        
        sql = f"SELECT id, nombre, correo, tipo, metrica_pago FROM empleado WHERE correo = {marca}"
        cursor.execute(sql, (correo,))
        fila = cursor.fetchone()
        conexion.close()
        
        return EmpleadoDAO._fila_a_empleado(fila) if fila else None

    @staticmethod
    def listar() -> list:
        """Recupera todos los empleados con la suma de sus horas acumuladas desde la BD"""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        sql = """
            SELECT e.id, e.nombre, e.correo, e.tipo, e.metrica_pago, COALESCE(SUM(r.horas), 0.0) as horas_totales
            FROM empleado e
            LEFT JOIN registro_trabajo r ON e.id = r.empleado_id
            GROUP BY e.id
        """
        cursor.execute(sql)
        filas = cursor.fetchall()
        conexion.close()
        
        empleados_reconstruidos = []
        for fila in filas:
            id_emp, nombre, email, tipo, metrica_pago, horas_totales = fila
            
            if tipo == "PorHora":
                emp = EmpleadoPorHora(nombre, email, valor_hora=float(metrica_pago))
                emp.id_empleado = id_emp
                emp.registrar_horas(horas_totales)
            else:
                emp = EmpleadoMensual(nombre, email, salario_mensual=float(metrica_pago))
                emp.id_empleado = id_emp
                
            empleados_reconstruidos.append(emp)
            
        return empleados_reconstruidos
    @staticmethod
    def actualizar(empleado: Empleado) -> bool:
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            sql = f"UPDATE empleado SET nombre = {marca}, correo = {marca} WHERE id = {marca}"
            cursor.execute(sql, (empleado.nombre, empleado.email, empleado.id_empleado))
            conexion.commit()
            return cursor.rowcount > 0  # Comprobación de filas afectadas por rowcount
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(id_empleado: str) -> bool:
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            sql = f"DELETE FROM empleado WHERE id = {marca}"
            cursor.execute(sql, (id_empleado,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()