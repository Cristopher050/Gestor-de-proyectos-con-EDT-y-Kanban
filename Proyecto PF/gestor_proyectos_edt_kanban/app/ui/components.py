"""Interfaz ReactPy. Los eventos llaman a lógica pura y después a SQLite."""
from reactpy import component, html, use_state
from app.domain.logic import (
    ESTADOS, PRIORIDADES, crear_tarea, cambiar_estado, filtrar_tareas,
    filtro_por_estado, ordenar_por_prioridad, contar_por_estado, registrar_ejecucion
)
from app.domain.results import Ok, Error
from app.infrastructure.database import listar_tareas, guardar_tarea, actualizar_estado, eliminar_tarea

@component
def App():
    # Estado reactivo de la interfaz.
    tareas, set_tareas = use_state(listar_tareas())
    nombre, set_nombre = use_state("")
    entregable, set_entregable = use_state("1. Planificación")
    responsable, set_responsable = use_state("")
    prioridad, set_prioridad = use_state("Media")
    fecha, set_fecha = use_state("")
    busqueda, set_busqueda = use_state("")
    mensaje, set_mensaje = use_state("")
    filtro_responsable, set_filtro_responsable = use_state("Todos")

    @registrar_ejecucion
    def recargar():
        set_tareas(listar_tareas())

    def agregar(evento):
        resultado = crear_tarea(nombre, entregable, responsable, prioridad, fecha)
        match resultado:
            case Ok(valor=tarea):
                guardada = guardar_tarea(tarea)
                set_tareas([guardada] + tareas)
                set_nombre("")
                set_responsable("")
                set_fecha("")
                set_mensaje("Tarea creada correctamente.")
            case Error(mensaje=error):
                set_mensaje(error)

    def mover(tarea, estado):
        resultado = cambiar_estado(tarea, estado)
        match resultado:
            case Ok(valor=actualizada):
                actualizar_estado(tarea.id, actualizada.estado)
                set_tareas([actualizada if t.id == tarea.id else t for t in tareas])
                set_mensaje("Estado actualizado.")
            case Error(mensaje=error):
                set_mensaje(error)

    def borrar(tarea_id):
        eliminar_tarea(tarea_id)
        set_tareas([t for t in tareas if t.id != tarea_id])
        set_mensaje("Tarea eliminada.")

    filtradas = filtrar_tareas(
        ordenar_por_prioridad(tareas),
        lambda t: (busqueda.lower() in t.nombre.lower()
                   or busqueda.lower() in t.entregable.lower())
                  and (filtro_responsable == "Todos" or t.responsable == filtro_responsable)
    )
    conteo = contar_por_estado(tareas)
    responsables = ["Todos"] + sorted({t.responsable for t in tareas})

    def campo(etiqueta, valor, setter, placeholder="", tipo="text"):
        return html.label({"class_name": "campo"}, etiqueta,
            html.input({"type": tipo, "value": valor, "placeholder": placeholder,
                        "on_change": lambda evento: setter(evento["target"]["value"])}))

    def tarjeta(tarea):
        return html.article({"class_name": "tarjeta", "key": str(tarea.id)},
            html.div({"class_name": "tarjeta-cabecera"},
                html.strong(tarea.nombre),
                html.button({"class_name": "eliminar", "title": "Eliminar tarea",
                             "on_click": lambda evento, tid=tarea.id: borrar(tid)}, "×")),
            html.p({"class_name": "meta"}, f"EDT: {tarea.entregable}"),
            html.p({"class_name": "meta"}, f"Responsable: {tarea.responsable}"),
            html.div({"class_name": "etiquetas"},
                html.span({"class_name": "prioridad " + tarea.prioridad.lower()}, tarea.prioridad),
                html.span({"class_name": "fecha"}, "Sin fecha" if not tarea.fecha_limite else tarea.fecha_limite)),
            html.label("Cambiar estado"),
            html.select({"value": tarea.estado,
                         "on_change": lambda evento, t=tarea: mover(t, evento["target"]["value"])},
                *[html.option({"value": estado}, estado) for estado in ESTADOS])
        )

    return html.div({"class_name": "app"},
        html.header({"class_name": "hero"},
            html.div({"class_name": "hero-contenido"},
                html.p({"class_name": "sobrelinea"}, "PLANIFICACIÓN · EDT · KANBAN"),
                html.h1("Gestor de proyectos"),
                html.p("Organiza entregables, asigna responsables y sigue el avance del equipo."))),
        html.main(
            html.section({"class_name": "resumen"},
                *[html.div({"class_name": "estadistica"},
                    html.span(estado), html.strong(str(conteo[estado])))
                  for estado in ESTADOS]),
            html.section({"class_name": "panel formulario-panel"},
                html.div({"class_name": "titulo-panel"},
                    html.div(html.h2("Nueva tarea"), html.p("Cada tarea se vincula a un elemento de la EDT."))),
                html.div({"class_name": "formulario"},
                    html.div({"class_name": "form-grid"},
                        campo("Nombre de la tarea", nombre, set_nombre, "Ej. Investigar requisitos"),
                        campo("Entregable / EDT", entregable, set_entregable, "Ej. 1.1 Requisitos"),
                        campo("Responsable", responsable, set_responsable, "Nombre del integrante"),
                        html.label({"class_name": "campo"}, "Prioridad",
                            html.select({"value": prioridad, "on_change": lambda e: set_prioridad(e["target"]["value"])},
                                *[html.option({"value": p}, p) for p in PRIORIDADES])),
                        campo("Fecha límite (opcional)", fecha, set_fecha, "", "date")),
                    html.button({"class_name": "boton-principal", "on_click": agregar}, "＋ Crear tarea"),
                    html.p({"class_name": "mensaje"}, mensaje))),
            html.section({"class_name": "panel herramientas"},
                html.div(html.h2("Tablero Kanban"), html.p("La EDT describe el trabajo; Kanban muestra su estado.")),
                html.div({"class_name": "filtros"},
                    html.input({"value": busqueda, "placeholder": "Buscar tarea o entregable…",
                                "on_change": lambda e: set_busqueda(e["target"]["value"])}),
                    html.select({"value": filtro_responsable,
                                 "on_change": lambda e: set_filtro_responsable(e["target"]["value"])},
                        *[html.option({"value": r}, r) for r in responsables]))),
            html.section({"class_name": "kanban"},
                *[html.div({"class_name": "columna " + estado.lower().replace(" ", "-"), "key": estado},
                    html.div({"class_name": "columna-titulo"},
                        html.h3(estado), html.span({"class_name": "contador"},
                            str(len(filtrar_tareas(filtradas, filtro_por_estado(estado)))))),
                    html.div({"class_name": "lista-tarjetas"},
                        *[tarjeta(t) for t in filtrar_tareas(filtradas, filtro_por_estado(estado))])
                  ) for estado in ESTADOS]),
            html.footer("Proyecto académico de Programación Funcional · ReactPy + FastAPI + SQLite")
        )
    )
