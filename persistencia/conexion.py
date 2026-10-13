import os
import sqlite3

def obtener_motor() -> str:
    return os.getenv("DB_MOTOR", "sqlite").lower()

def abrir_conexion():
    motor = obtener_motor()
    if motor == "sqlite":
        ruta = os.getenv("DB_RUTA", "ecotech.db")
        return sqlite3.connect(ruta)
    elif motor == "mysql":
        import pymysql
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "ecotech_db")
        )
    raise ValueError(f"Motor '{motor}' no soportado.")

def marcador_sql() -> str:
    
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"