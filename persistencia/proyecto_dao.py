from dependencia.proyecto import Proyecto
from persistencia.conexion import abrir_conexion, marcador_sql

class ProyectoDAO:
    
    @staticmethod
    def _fila_a_proyecto(fila: tuple) -> Proyecto:
        """Helper interno encapsulado para reconstruir objetos Proyecto desde registros SQL"""
        if not fila:
            return None
        nombre, descripcion = fila
        return Proyecto(nombre, descripcion)

    @staticmethod
    def insertar(proy: Proyecto) -> bool:
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            sql = f"INSERT INTO proyecto (nombre, descripcion) VALUES ({marca}, {marca})"
            cursor.execute(sql, (proy.nombre, proy.descripcion))
            conexion.commit()  # Confirma la transacción de forma segura
            return True
        except Exception:
            if conexion:
                conexion.rollback()  # Revierte los cambios ante fallas en la BD
            raise
        finally:
            if conexion:
                conexion.close()  # Libera los recursos del sistema siempre

    @staticmethod
    def buscar_por_nombre(nombre: str) -> Proyecto:
        """Busca un proyecto específico por su nombre (Llave Primaria)"""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marca = marcador_sql()
        
        sql = f"SELECT nombre, descripcion FROM proyecto WHERE nombre = {marca}"
        cursor.execute(sql, (nombre,))
        fila = cursor.fetchone() 
        conexion.close()
        
        return ProyectoDAO._fila_a_proyecto(fila) if fila else None

    @staticmethod
    def listar() -> list:
        """Recupera todos los proyectos almacenados en la Base de Datos"""
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        sql = "SELECT nombre, descripcion FROM proyecto"
        cursor.execute(sql)
        filas = cursor.fetchall()  
        conexion.close()
        
       
        return [ProyectoDAO._fila_a_proyecto(f) for f in filas]

    @staticmethod
    def actualizar(proy: Proyecto) -> bool:
        """Actualiza la descripción de un proyecto existente"""
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            sql = f"UPDATE proyecto SET descripcion = {marca} WHERE nombre = {marca}"
            cursor.execute(sql, (proy.descripcion, proy.nombre))
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
        """Elimina un proyecto de la base de datos por su nombre"""
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            sql = f"DELETE FROM proyecto WHERE nombre = {marca}"
            cursor.execute(sql, (nombre,))
            conexion.commit()
            return cursor.rowcount > 0  # Evita confundir ausencia con error real
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()