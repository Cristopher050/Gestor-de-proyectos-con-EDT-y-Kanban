"""Modelos inmutables del dominio. No acceden a archivos, red ni base de datos."""
from dataclasses import dataclass
from typing import Optional, Literal

Estado = Literal["Pendiente", "En progreso", "Completada"]
Prioridad = Literal["Baja", "Media", "Alta"]

@dataclass(frozen=True)
class Proyecto:
    nombre: str
    descripcion: str = ""

@dataclass(frozen=True)
class Tarea:
    id: int
    nombre: str
    entregable: str
    responsable: str
    prioridad: Prioridad
    estado: Estado = "Pendiente"
    fecha_limite: Optional[str] = None
