"""Punto de entrada: FastAPI sirve la interfaz ReactPy; no se crea una API REST propia."""
from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from app.infrastructure.database import inicializar_db
from app.ui.components import App

inicializar_db()
app = FastAPI(title="Gestor de proyectos EDT y Kanban")
configure(app, App)
