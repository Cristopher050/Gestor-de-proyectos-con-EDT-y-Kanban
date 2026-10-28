# Gestor de proyectos con EDT y Kanban

Aplicación web local para planificar tareas, vincularlas a entregables de una EDT y controlar su estado mediante un tablero Kanban.

## Requisitos
- Python 3.10 o superior (se recomienda Python 3.11 o 3.12).
- Internet durante la primera instalación para descargar dependencias.
- Navegador web moderno.

## Instalación en Windows (PowerShell)
1. Descomprime el proyecto y abre una terminal dentro de la carpeta `gestor_proyectos_edt_kanban`.
2. Crea el entorno virtual:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea la activación, ejecuta `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` y luego usa `.\.venv\Scripts\python.exe` para los siguientes comandos.

3. Instala las dependencias:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Inicia la aplicación:

   ```powershell
   python -m uvicorn app.main:app --reload
   ```

5. Abre en el navegador la dirección que muestra Uvicorn, normalmente `http://127.0.0.1:8000`.

La base `gestor.db` se crea automáticamente en la carpeta raíz la primera vez que se inicia la aplicación. No la borres si quieres conservar las tareas.

## Ejecutar las pruebas
```powershell
python -m unittest discover -s tests -v
```

## Funciones disponibles
- Crear tareas con entregable EDT, responsable, prioridad y fecha límite opcional.
- Cambiar entre Pendiente, En progreso y Completada.
- Buscar por nombre o entregable.
- Filtrar por responsable.
- Ordenar las tareas por prioridad.
- Eliminar tareas.
- Guardar los datos en SQLite para conservarlos al reiniciar.

## Arquitectura
- `app/domain/`: modelos inmutables y reglas puras.
- `app/infrastructure/`: persistencia SQLite (efectos secundarios).
- `app/ui/`: interfaz ReactPy.
- `app/main.py`: integración y servidor FastAPI. No se define una API REST propia.

## Evidencias de Programación Funcional
1. **Funciones de orden superior:** `filtrar_tareas` recibe un criterio funcional.
2. **Lambda:** filtros y ordenación por prioridad.
3. **Closure:** `filtro_por_estado` devuelve una función que recuerda el estado.
4. **Pattern matching:** `match/case` en `cambiar_estado` y al procesar `Resultado`.
5. **Inmutabilidad:** `Tarea` usa `@dataclass(frozen=True)` y `replace` crea una nueva instancia.
6. **Pureza:** `crear_tarea`, `cambiar_estado`, `filtrar_tareas` no acceden a SQLite ni modifican datos externos.
7. **Ausencia de valor:** `fecha_limite` puede ser `None` si no se especifica.
8. **Errores como valor:** `Ok` y `Error` evitan depender de excepciones para las validaciones del dominio.
9. **Decoradores:** `@component` en ReactPy y `@registrar_ejecucion` en `recargar`.
10. **Efectos secundarios:** operaciones de SQLite y eventos de interfaz están fuera del núcleo funcional.

## EDT sugerida para una demostración
- 1. Planificación
  - 1.1 Definir alcance
  - 1.2 Identificar responsables
- 2. Diseño
  - 2.1 Diseñar interfaz
  - 2.2 Definir estructura de datos
- 3. Desarrollo
  - 3.1 Crear tareas
  - 3.2 Implementar tablero
- 4. Pruebas y entrega
  - 4.1 Ejecutar pruebas
  - 4.2 Preparar presentación

En la aplicación, escribe el número y nombre del entregable en el campo “Entregable / EDT”. Esto representa la relación visible de cada tarea con la EDT.

## Trabajo en equipo (2 integrantes)
- Integrante 1: dominio funcional, validaciones, manejo de errores y pruebas (`app/domain/`, `tests/`).
- Integrante 2: interfaz ReactPy, SQLite e integración (`app/ui/`, `app/infrastructure/`, `app/main.py`).
- Ambos: revisar cambios, probar la aplicación, documentar decisiones y participar en el video.

## Git y GitHub
Cada integrante debe trabajar con su propia cuenta o identidad Git configurada. Usen ramas y pull requests cuando sea posible, y realicen commits reales sobre las partes que cada persona desarrolló. No creen commits ficticios para aparentar contribuciones.

## Limitaciones conocidas de esta versión académica
- Es una versión local y sencilla, sin inicio de sesión ni permisos.
- La EDT se representa con el código/nombre del entregable asociado a cada tarea; no incluye un editor gráfico jerárquico.
- El cambio de estado se realiza mediante una lista desplegable en cada tarjeta, no arrastrando tarjetas.
- La aplicación es para demostración académica y no está endurecida para uso en producción.
