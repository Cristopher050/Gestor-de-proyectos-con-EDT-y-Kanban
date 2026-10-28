"""Imperative Shell: SQLite es un efecto secundario aislado aquí."""
import sqlite3
from pathlib import Path
from typing import List
from app.domain.models import Tarea

DB_PATH = Path(__file__).resolve().parents[2] / "gestor.db"

def conectar():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_db():
    with conectar() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                entregable TEXT NOT NULL,
                responsable TEXT NOT NULL,
                prioridad TEXT NOT NULL,
                estado TEXT NOT NULL,
                fecha_limite TEXT
            )
        """)

def listar_tareas() -> List[Tarea]:
    with conectar() as db:
        filas = db.execute("SELECT * FROM tareas ORDER BY id DESC").fetchall()
    return [Tarea(
        id=f["id"], nombre=f["nombre"], entregable=f["entregable"],
        responsable=f["responsable"], prioridad=f["prioridad"],
        estado=f["estado"], fecha_limite=f["fecha_limite"]
    ) for f in filas]

def guardar_tarea(tarea: Tarea) -> Tarea:
    with conectar() as db:
        cursor = db.execute("""
            INSERT INTO tareas (nombre, entregable, responsable, prioridad, estado, fecha_limite)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tarea.nombre, tarea.entregable, tarea.responsable,
              tarea.prioridad, tarea.estado, tarea.fecha_limite))
        nuevo_id = cursor.lastrowid
    from dataclasses import replace
    return replace(tarea, id=nuevo_id)

def actualizar_estado(tarea_id: int, estado: str) -> None:
    with conectar() as db:
        db.execute("UPDATE tareas SET estado = ? WHERE id = ?", (estado, tarea_id))

def eliminar_tarea(tarea_id: int) -> None:
    with conectar() as db:
        db.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
