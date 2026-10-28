"""Manejo funcional de errores: el resultado expresa éxito o error como un valor."""
from dataclasses import dataclass
from typing import Generic, TypeVar, Union

T = TypeVar("T")

@dataclass(frozen=True)
class Ok(Generic[T]):
    valor: T

@dataclass(frozen=True)
class Error:
    mensaje: str

Resultado = Union[Ok[T], Error]
