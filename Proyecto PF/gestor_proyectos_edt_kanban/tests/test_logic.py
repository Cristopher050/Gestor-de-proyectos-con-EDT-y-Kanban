import unittest
from app.domain.logic import crear_tarea, cambiar_estado, filtrar_tareas, filtro_por_estado
from app.domain.models import Tarea
from app.domain.results import Ok, Error

class TestLogicaFuncional(unittest.TestCase):
    def setUp(self):
        self.tarea = Tarea(1, "Diseñar interfaz", "2. Diseño", "Ana", "Alta")

    def test_crear_tarea_correcta(self):
        resultado = crear_tarea("  Diseñar interfaz ", "2. Diseño", "Ana", "Alta")
        self.assertIsInstance(resultado, Ok)
        self.assertEqual(resultado.valor.nombre, "Diseñar interfaz")

    def test_rechaza_nombre_vacio(self):
        self.assertIsInstance(crear_tarea("", "Diseño", "Ana", "Media"), Error)

    def test_cambiar_estado_no_mutable(self):
        resultado = cambiar_estado(self.tarea, "Completada")
        self.assertIsInstance(resultado, Ok)
        self.assertEqual(resultado.valor.estado, "Completada")
        self.assertEqual(self.tarea.estado, "Pendiente")

    def test_closure_filtra_estado(self):
        tareas = [self.tarea, Tarea(2, "Probar", "3. Pruebas", "Luis", "Media", "Completada")]
        completadas = filtrar_tareas(tareas, filtro_por_estado("Completada"))
        self.assertEqual([t.id for t in completadas], [2])

if __name__ == "__main__":
    unittest.main()
