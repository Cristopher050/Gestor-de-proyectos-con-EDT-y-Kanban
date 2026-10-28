"""Functional Core: funciones deterministas que solo transforman datos."""
from dataclasses import replace
from typing import Callable, Iterable, List, Sequence
from .models import Tarea
from .results import Error, Ok, Resultado

ESTADOS = ("Pendiente", "En progreso", "Completada")
PRIORIDADES = ("Baja", "Media", "Alta")

def normalizar_texto(texto: str) -> str:
    return " ".join(texto.strip().split())

def crear_tarea(nombre: str, entregable: str, responsable: str,
                prioridad: str, fecha_limite: str = "") -> Resultado[Tarea]:
    nombre = normalizar_texto(nombre)
    entregable = normalizar_texto(entregable)
    responsable = normalizar_texto(responsable)
    if not nombre:
        return Error("Escribe un nombre para la tarea.")
    if not entregable:
        return Error("Escribe el entregable o elemento de la EDT.")
    if not responsable:
        return Error("Indica quién será responsable.")
    if prioridad not in PRIORIDADES:
        return Error("Selecciona una prioridad válida.")
    return Ok(Tarea(
        id=0, nombre=nombre, entregable=entregable, responsable=responsable,
        prioridad=prioridad, estado="Pendiente",
        fecha_limite=fecha_limite.strip() or None
    ))

def cambiar_estado(tarea: Tarea, nuevo_estado: str) -> Resultado[Tarea]:
    # Pattern matching (match/case) para describir los estados admitidos.
    match nuevo_estado:
        case "Pendiente" | "En progreso" | "Completada":
            return Ok(replace(tarea, estado=nuevo_estado))
        case _:
            return Error("El estado seleccionado no es válido.")

def filtrar_tareas(tareas: Sequence[Tarea],
                   criterio: Callable[[Tarea], bool]) -> List[Tarea]:
    """Función de orden superior: recibe otra función como criterio."""
    return [tarea for tarea in tareas if criterio(tarea)]

def filtro_por_estado(estado: str) -> Callable[[Tarea], bool]:
    """Closure: la función devuelta recuerda el estado recibido."""
    return lambda tarea: tarea.estado == estado

def ordenar_por_prioridad(tareas: Sequence[Tarea]) -> List[Tarea]:
    peso = {"Alta": 0, "Media": 1, "Baja": 2}
    return sorted(tareas, key=lambda tarea: peso[tarea.prioridad])

def contar_por_estado(tareas: Iterable[Tarea]) -> dict:
    conteo = {estado: 0 for estado in ESTADOS}
    for tarea in tareas:
        conteo[tarea.estado] += 1
    return conteo

def registrar_ejecucion(funcion):
    """Decorador sencillo para mostrar evidencia de una operación ejecutada."""
    def envoltura(*args, **kwargs):
        print(f"[LOG] Ejecutando {funcion.__name__}")
        return funcion(*args, **kwargs)
    return envoltura
