from dependencia.empleado import EmpleadoMensual, EmpleadoPorHora
from persistencia.empleado_dao import EmpleadoDAO
from dependencia.registro_trabajo import RegistroTrabajo
from persistencia.registro_trabajo_dao import RegistroTrabajoDAO
from persistencia.proyecto_dao import ProyectoDAO

def solicitar_opcion_empleado() -> int:
    """Implementa Validación + Excepción simultáneamente tal como pide la Clase 7"""
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion < 0 or opcion > 6:
                print("[Validación] Opción fuera de rango (0 a 6). Intente nuevamente.")
                continue
            return opcion
        except ValueError:
            print("[Excepción] Entrada incorrecta. Debe escribir obligatoriamente un número entero.")

def ejecutar_registro():
    print("\n--- REGISTRAR EMPLEADO ---")
    nombre = input("Nombre: ").strip()
    correo = input("Correo: ").strip()
    
    if not nombre or not correo:
        print("[Validación] El nombre y el correo no pueden estar vacíos.")
        return

    # Validación anti-duplicados consultando a la persistencia mediante Clave Natural (Email)
    try:
        if EmpleadoDAO.buscar_por_correo(correo) is not None:
            print(f"[Validación] Registro denegado: El correo '{correo}' ya existe en el sistema.")
            return
    except Exception:
        print("[Error de Persistencia] No se pudo verificar la unicidad del correo.")
        return

    print("Tipo contrato: 1) Mensual  2) Por Hora")
    tipo = input("Opción: ").strip()
    
    if tipo == "1":
        try:
            sueldo = float(input("Sueldo Mensual ($): "))
            empleado = EmpleadoMensual(nombre, correo, sueldo)
        except ValueError:
            print("[Validación] El sueldo debe ser una cantidad numérica.")
            return
    elif tipo == "2":
        try:
            valor_hora = float(input("Valor Hora ($): "))
            empleado = EmpleadoPorHora(nombre, correo, valor_hora)
        except ValueError:
            print("[Validación] El valor hora debe ser una cantidad numérica.")
            return
    else:
        print("[Validación] Tipo de contrato inválido.")
        return

    # Inserción controlada
    try:
        if EmpleadoDAO.insertar(empleado):
            print(f"¡Empleado registrado correctamente con ID: {empleado.id_empleado}!")
    except Exception:
        print("[Error Seguro] No fue posible guardar el registro en la base de datos.")

def ejecutar_listado():
    print("\n--- LISTADO DE EMPLEADOS ---")
    try:
        empleados = EmpleadoDAO.listar()
        if not empleados:
            print("No hay empleados guardados.")
            return
        for emp in empleados:
            print(emp.mostrar_datos())
    except Exception:
        print("[Error Seguro] Fallo de conectividad al listar.")

def ejecutar_busqueda():
    print("\n--- BUSCAR EMPLEADO ---")
    id_buscar = input("Ingrese ID de empleado: ").strip()
    try:
        emp = EmpleadoDAO.buscar_por_id(id_buscar)
        if emp:
            print(f"Encontrado -> {emp.mostrar_datos()}")
        else:
            print("[Aviso] Empleado no encontrado.")  # Resultado normal sin lanzar excepción
    except Exception:
        print("[Error Seguro] Falló la consulta transaccional.")

def ejecutar_actualizacion():
    print("\n--- ACTUALIZAR EMPLEADO ---")
    id_modificar = input("Ingrese ID del empleado a cambiar: ").strip()
    try:
        emp = EmpleadoDAO.buscar_por_id(id_modificar)
        if not emp:
            print("[Aviso] El empleado especificado no existe.")
            return
        
        nuevo_nombre = input(f"Nuevo Nombre [{emp.nombre}]: ").strip()
        nuevo_correo = input(f"Nuevo Correo [{emp.email}]: ").strip()
        
        if nuevo_nombre: emp.nombre = nuevo_nombre
        if nuevo_correo: emp.email = nuevo_correo
        
        if EmpleadoDAO.actualizar(emp):
            print("¡Datos actualizados de forma exitosa!")
        else:
            print("[Aviso] No se alteró ningún registro.")
    except Exception:
        print("[Error Seguro] No se pudo procesar la actualización.")

def ejecutar_eliminacion():
    """Mini desafío Clase 6: Eliminar sin confundir ausencia con error real"""
    print("\n--- ELIMINAR EMPLEADO ---")
    id_borrar = input("Ingrese ID a remover: ").strip()
    try:
        removido = EmpleadoDAO.eliminar(id_borrar)
        if removido:
            print(f"¡El empleado con ID {id_borrar} ha sido eliminado satisfactoriamente!")
        else:
            print(f"[Aviso] Operación cancelada: El ID {id_borrar} no existe.")  # Ausencia ordinaria
    except Exception:
        print("[Error Crítico] Restricción de integridad violada o fallo del servidor.")  # Excepción real

def ejecutar_registro_horas():
    print("\n--- REGISTRAR HORAS TRABAJADAS (EcoTech) ---")
    
    # 1. Validar que el empleado exista en la BD
    id_emp = input("Ingrese el ID del Empleado: ").strip()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_emp)
        if not empleado:
            print("[Validación] El empleado con ese ID no existe.")
            return
    except Exception:
        print("[Error Seguro] No se pudo verificar el empleado.")
        return
    nombre_proy = input("Ingrese el Nombre del Proyecto: ").strip()
    try:
        proyecto = ProyectoDAO.buscar_por_nombre(nombre_proy)
        if not proyecto:
            print("[Validación] El proyecto especificado no está registrado.")
            return
    except Exception:
        print("[Error Seguro] No se pudo verificar el proyecto.")
        return

    try:
        horas = float(input("Cantidad de horas trabajadas: "))
        if horas <= 0:
            print("[Validación] Las horas deben ser un número mayor a cero.")
            return
    except ValueError:
        print("[Excepción] Debe ingresar un número válido para las horas.")
        return

    fecha = input("Fecha (AAAA-MM-DD): ").strip()
    descripcion = input("Descripción de la tarea: ").strip()

    nuevo_registro = RegistroTrabajo(fecha, horas, descripcion, empleado, proyecto)

    try:
        if RegistroTrabajoDAO.insertar(nuevo_registro):
            print(f"¡Éxito! Se registraron {horas} horas para {empleado.nombre} en el proyecto '{proyecto.nombre}'.")
            
            if isinstance(empleado, EmpleadoPorHora):
                empleado.registrar_horas(horas)
                print(f"[Cálculo] Nuevo sueldo acumulado por hora: ${empleado.calcular_pago():,}")
    except Exception:
        print("[Error Crítico] Falló el guardado transaccional en la tabla 'registro_trabajo'.")


def menu_empleado():
    while True:
        print("\n=== MÓDULO: GESTIÓN DE EMPLEADOS ===")
        print("1. Registrar nuevo empleado")
        print("2. Listar todos los empleados")
        print("3. Buscar empleado por ID")
        print("4. Actualizar datos de empleado")
        print("5. Eliminar empleado de la empresa")
        print("6. Registrar horas de empleado por horas")
        print("0. Volver al Menú Principal")
        
        opcion = solicitar_opcion_empleado()
        
        if opcion == 1: ejecutar_registro()
        elif opcion == 2: ejecutar_listado()
        elif opcion == 3: ejecutar_busqueda()
        elif opcion == 4: ejecutar_actualizacion()
        elif opcion == 5: ejecutar_eliminacion()
        elif opcion == 6: ejecutar_registro_horas()
        elif opcion == 0: break
