from dependencia.registro_trabajo import RegistroTrabajo
from persistencia.conexion import abrir_conexion, marcador_sql

class RegistroTrabajoDAO:
    @staticmethod
    def insertar(reg: RegistroTrabajo) -> bool:
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            sql = f"INSERT INTO registro_trabajo (fecha, horas, descripcion, empleado_id, proyecto_nombre) VALUES ({marca}, {marca}, {marca}, {marca}, {marca})"
            cursor.execute(sql, (reg.fecha, reg.horas, reg.descripcion, reg.empleado.id_empleado, reg.proyecto.nombre))
            conexion.commit()
            return True
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()