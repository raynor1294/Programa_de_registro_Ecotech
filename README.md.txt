# EcoTech Solutions - Sistema de Gestión Interna (Desarrollo Individual)

Este sistema implementa una solución de software orientada a objetos (POO) y una arquitectura de persistencia transaccional robusta para mitigar las problemáticas de duplicidad de información, falta de trazabilidad y errores de asignación de personal en **EcoTech Solutions**.

## 1. Arquitectura del Proyecto (3 Capas)

El software adopta una arquitectura en capas que separa de forma estricta las responsabilidades, garantizando la mantenibilidad y escalabilidad del sistema:

*   **Capa de Dominio (`src/dependencia/`):** Contiene los modelos puros y la lógica empresarial (`Empleado`, `Departamento`, `Proyecto`, `RegistroTrabajo`). Aquí se procesa la herencia, el polimorfismo y las reglas del negocio sin interferencia de código SQL ni menús.
*   **Capa de Persistencia (`src/persistencia/`):** Implementa el patrón **DAO (Data Access Object)** con métodos estáticos. Centraliza las consultas parametrizadas a la base de datos, manejando los ciclos de vida de las conexiones.
*   **Capa de Interacción (`src/menus/` y `src/main.py`):** Controla el flujo de las pantallas en consola, captura datos del usuario y diferencia la validación de entradas ordinarias del manejo de excepciones críticas.

---

## 2. Responsabilidad de Desarrollo (Full-Stack)

Al ser un proyecto de ejecución individual, asumí la autoría e integración de todos los componentes nucleares del sistema descritos en las convenciones del curso (Clases 1 a 8):
*   **Gestión de Personal:** Implementación de la jerarquía polimórfica de empleados (`Mensual` y `PorHora`) con ID único automatizado por `uuid`.
*   **Gestión Operativa:** Modelado y control de las entidades `Proyecto` y `Departamento`, resolviendo de forma relacional la asociación del **Rol de Gerente**.
*   **Persistencia Completa (CRUD):** Desarrollo de consultas SQL seguras y parametrizadas, incorporando un subproceso relacional (`LEFT JOIN` y `SUM`) para actualizar los pagos calculados de los trabajadores en tiempo real directamente desde el motor de datos.

---

## 3. Justificación Técnica y Mitigación de Errores de la IA

*   **Modelado Relacional vs. Modelos Planos de IA:** A diferencia de los diseños generados por Inteligencia Artificial que tienden a acoplar el código mezclando SQL dentro del dominio, este diseño separa estrictamente ambas capas. Se materializó la relación de muchos a muchos mediante la clase asociativa `RegistroTrabajo`, logrando una trazabilidad absoluta de las horas de la empresa.
*   **Encapsulamiento Riguroso:** Las colecciones internas de datos se marcan como privadas (`_`) y se exponen externamente como **tuplas inmutables (`tuple`)** mediante el decorador `@property`, bloqueando alteraciones accidentales externas desde los menús de interacción.
*   **Transacciones Seguras (Commit/Rollback):** Las operaciones de escritura en los DAOs están protegidas por bloques `try/except/finally`. Si una inserción falla (ej. restricción de correo único duplicado), se ejecuta un `rollback()` automático para mantener la consistencia de la base de datos.

---

## 4. Guía de Ejecución en un Entorno Limpio (Laboratorio)

Siga estos pasos exactos en la terminal para levantar el proyecto de forma autónoma en los equipos del laboratorio:

1. **Sitúese en la raíz del proyecto:**
   ```bash
   cd ecotech-poos
   ```
2. **Cree y active el entorno virtual aislado (`.venv`)**:
   * En Windows (Git Bash): `source .venv/Scripts/activate`
   * En Windows (PowerShell): `.venv\Scripts\Activate.ps1`
3. **Instale las dependencias oficiales del curso:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure sus variables en el archivo `.env`** (Copie los valores base de `.env.example`).
5. **Ejecute el orquestador principal:**
   ```bash
   python src/main.py
   ```