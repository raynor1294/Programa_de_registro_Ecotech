from dependencia.departamento import Departamento
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO

def solicitar_opcion_depto() -> int:
    """Implementa Validación + Excepción simultáneamente (Clase 7 y 8)"""
    while True:
        try:
            opcion = int(input("Seleccione una opción de departamentos: "))
            if opcion < 0 or opcion > 3:
                print("[Validación] Opción fuera de rango (0 a 3). Intente de nuevo.")
                continue
            return opcion
        except ValueError:
            print("[Excepción] Entrada incorrecta. Debe ingresar un número entero.")

def registrar_departamento():
    print("\n--- REGISTRAR NUEVO DEPARTAMENTO ---")
    nombre = input("Nombre del Departamento: ").strip()
    
    if not nombre:
        print("[Validación] El nombre del departamento es obligatorio.")
        return

    # Validación anti-duplicados por Clave Primaria (Nombre)
    try:
        if DepartamentoDAO.buscar_por_nombre(nombre) is not None:
            print(f"[Validación] Registro denegado: El departamento '{nombre}' ya existe.")
            return
    except Exception:
        print("[Error de Persistencia] No se pudo verificar la existencia previa.")
        return

    depto = Departamento(nombre)

    # Lógica de asignación de Gerente (Asociación de Rol del UML)
    print("¿Desea asignar un gerente en este momento? (s/n)")
    if input().lower().strip() == 's':
        id_gerente = input("Ingrese el ID único del empleado que será Gerente: ").strip()
        try:
            empleado = EmpleadoDAO.buscar_por_id(id_gerente)
            if empleado:
                depto.assignar_gerente(empleado) if hasattr(depto, 'assignar_gerente') else depto.asignar_gerente(empleado)
                print(f"[Asociación] {empleado.nombre} ha sido asignado con el rol de Gerente.")
            else:
                print("[Aviso Normal] El ID no corresponde a ningún empleado registrado. Se creará sin gerente.")
        except Exception:
            print("[Error Seguro] Falló la verificación del empleado en el subsistema de datos.")

    try:
        if DepartamentoDAO.insertar(depto):
            print(f"¡Departamento '{nombre}' registrado exitosamente en el sistema!")
    except Exception:
        print("[Error Seguro] Error de persistencia al guardar el departamento.")

def listar_departamentos():
    print("\n--- LISTADO DE DEPARTAMENTOS ECOTECH (BD) ---")
    try:
        lista = DepartamentoDAO.listar()
        if not lista:
            print("No existen departamentos registrados actualmente en el sistema.")
        else:
            for index, dep in enumerate(lista, 1):
                gerente_info = dep.gerente.nombre if dep.gerente else "Sin Gerente Asignado"
                print(f"{index}. Departamento: {dep.nombre} | Gerente Líder: {gerente_info}")
    except Exception:
        print("[Error Seguro] No fue posible recuperar el listado desde la base de datos.")
    
    input("\nPresione Enter para continuar...")

def asignar_gerente_a_existente():
    print("\n--- ASIGNAR GERENTE A DEPARTAMENTO EXISTENTE ---")
    nombre_dep = input("Ingrese el nombre del departamento: ").strip()
    try:
        dep = DepartamentoDAO.buscar_por_nombre(nombre_dep)
        if not dep:
            print("[Aviso] El departamento especificado no existe.")
            return
        
        id_gerente = input("Ingrese el ID del empleado que asumirá la jefatura: ").strip()
        empleado = EmpleadoDAO.buscar_por_id(id_gerente)
        
        if not empleado:
            print("[Aviso] El empleado especificado no existe.")
            return
            
        dep.asignar_gerente(empleado)
        if DepartamentoDAO.actualizar(dep):
            print(f"¡Éxito! {empleado.nombre} es ahora el nuevo Gerente de {dep.nombre}.")
        else:
            print("[Aviso] No se realizaron modificaciones en la persistencia.")
    except Exception:
        print("[Error Seguro] No fue posible actualizar la jefatura.")

def menu_departamento():
    while True:
        print("\n=== MÓDULO: GESTIÓN DE DEPARTAMENTOS ===")
        print("1. Registrar nuevo Departamento")
        print("2. Listar Departamentos activos")
        print("3. Asignar/Cambiar Gerente")
        print("0. Volver al Menú Principal")
        
        opcion = solicitar_opcion_depto()
        
        if opcion == 1:
            registrar_departamento()
        elif opcion == 2:
            listar_departamentos()
        elif opcion == 3:
            asignar_gerente_a_existente()
        elif opcion == 0:
            break