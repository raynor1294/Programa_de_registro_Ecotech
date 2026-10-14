from dependencia.departamento import Departamento
from persistencia.conexion import abrir_conexion, marcador_sql
from persistencia.empleado_dao import EmpleadoDAO

class DepartamentoDAO:
    
    @staticmethod
    def _fila_a_departamento(fila: tuple) -> Departamento:
        if not fila:
            return None
        nombre, gerente_id = fila
        dep = Departamento(nombre)
        
        # Si el departamento tiene un gerente asignado, el DAO lo busca y lo asocia
        if gerente_id:
            try:
                empleado_gerente = EmpleadoDAO.buscar_por_id(gerente_id)
                if empleado_gerente:
                    dep.asignar_gerente(empleado_gerente)
            except Exception:
                pass # Evita que un fallo al cargar el gerente rompa la carga del departamento
        return dep

    @staticmethod
    def insertar(dep: Departamento) -> bool:
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            sql = f"INSERT INTO departamento (nombre, gerente_id) VALUES ({marca}, {marca})"
            gerente_id = dep.gerente.id_empleado if dep.gerente else None
            
            cursor.execute(sql, (dep.nombre, gerente_id))
            conexion.commit()  # Transacción segura
            return True
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_nombre(nombre: str) -> Departamento:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()
        
        sql = f"SELECT nombre, gerente_id FROM departamento WHERE nombre = {marca}"
        cursor.execute(sql, (nombre,))
        fila = cursor.fetchone()
        conexion.close()
        
        return DepartamentoDAO._fila_a_departamento(fila) if fila else None

    @staticmethod
    def listar() -> list:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        sql = "SELECT nombre, gerente_id FROM departamento"
        cursor.execute(sql)
        filas = cursor.fetchall()
        conexion.close()
        
        return [DepartamentoDAO._fila_a_departamento(f) for f in filas]

    @staticmethod
    def actualizar(dep: Departamento) -> bool:
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            sql = f"UPDATE departamento SET gerente_id = {marca} WHERE nombre = {marca}"
            gerente_id = dep.gerente.id_empleado if dep.gerente else None
            
            cursor.execute(sql, (gerente_id, dep.nombre))
            conexion.commit()
            return cursor.rowcount > 0  # Control por rowcount
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(nombre: str) -> bool:
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            sql = f"DELETE FROM departamento WHERE nombre = {marca}"
            cursor.execute(sql, (nombre,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()