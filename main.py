import os
import sys

ruta_src = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta_src)

from menus.menu_empleado import menu_empleado
from menus.menu_proyecto import menu_proyecto
from menus.menu_departamento import menu_departamento

def inicializar_tablas_sqlite_local():
    import sqlite3
    conn = sqlite3.connect("ecotech.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleado (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            tipo TEXT NOT NULL,
            metrica_pago REAL NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departamento (
            nombre TEXT PRIMARY KEY,
            gerente_id TEXT,
            FOREIGN KEY(gerente_id) REFERENCES empleado(id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyecto (
            nombre TEXT PRIMARY KEY,
            descripcion TEXT
        )
    """)
    conn.commit()
    conn.close()

def main():
    if os.getenv("DB_MOTOR", "sqlite").lower() == "sqlite":
        inicializar_tablas_sqlite_local()
        
    while True:
        print("\n===============================================")
        print("  SISTEMA INTEGRADO DE GESTIÓN - ECOTECH ")
        print("===============================================")
        print("1. Módulo Gestión de Empleados")
        print("2. Módulo Gestión de Proyectos")
        print("3. Módulo Gestión de Departamentos")
        print("0. Cerrar Aplicación")
        print("===============================================")
        
        opcion = input("Seleccione una opción general: ").strip()
        
        if opcion == "1":
            menu_empleado()   
        elif opcion == "2":
            menu_proyecto()  
        elif opcion == "3":
            menu_departamento()
        elif opcion == "0":
            print("\nCierre de sesión seguro. ¡Hasta luego!")
            break
        else:
            print("[Validación] Opción inválida. Digite 1, 2, 3 o 0.")

if __name__ == "__main__":
    main()