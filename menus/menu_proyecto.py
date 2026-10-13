from dependencia.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDAO

def solicitar_opcion_proyecto() -> int:
    while True:
        try:
            opcion = int(input("Seleccione una opción de proyectos: "))
            if opcion < 0 or opcion > 2:
                print("[Validación] Opción fuera de rango (0 a 2).")
                continue
            return opcion
        except ValueError:
            print("[Excepción] Debe ingresar un número entero.")

def registrar_proyecto():
    print("\n--- REGISTRAR NUEVO PROYECTO ---")
    nombre = input("Nombre del Proyecto: ").strip()
    descripcion = input("Descripción / Alcance: ").strip()

    if not nombre:
        print("[Validación] El nombre del proyecto es obligatorio.")
        return

    nuevo_proy = Proyecto(nombre, descripcion)

    try:
        if ProyectoDAO.insertar(nuevo_proy):
            print(f"¡Proyecto '{nombre}' guardado con éxito en la Base de Datos!")
    except Exception:
        print("[Error Seguro] No se pudo conectar con la base de datos para registrar el proyecto.")

def listar_proyectos():
    print("\n--- LISTADO DE PROYECTOS ECOTECH (BD) ---")
    try:
        proyectos = ProyectoDAO.listar() 
        if not proyectos:
            print("No existen proyectos registrados actualmente en el sistema.")
        else:
            for index, proy in enumerate(proyectos, 1):
                print(f"{index}. Nombre: {proy.nombre} | Descripción: {proy.descripcion}")
    except Exception:
        print("[Error Seguro] No fue posible recuperar el listado de proyectos.")
    
    input("\nPresione Enter para continuar...")

def menu_proyecto():
    while True:
        print("\n=== MÓDULO: GESTIÓN DE PROYECTOS ===")
        print("1. Crear nuevo Proyecto")
        print("2. Listar Proyectos activos")
        print("0. Volver al Menú Principal")
        
        opcion = solicitar_opcion_proyecto()
        
        if opcion == 1:
            registrar_proyecto()
        elif opcion == 2:
            listar_proyectos()
        elif opcion == 0:
            break