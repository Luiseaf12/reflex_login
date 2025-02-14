import reflex as rx
from .state import ListState
from .add import add_department_button
from .edit import edit_department_button
from .search_department import search_dialog as search_department


def department_list() -> rx.Component:
    """Template que representa la lista completa de departamentos."""
    return rx.vstack(
        rx.hstack(
            rx.heading("Departamentos Disponibles", size="6"),
            width="100%",
            justify="between",
        ),
        add_department_button(),
        search_department(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("nombre"),
                    rx.table.column_header_cell("Estado"),
                    rx.table.column_header_cell("Acciones"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    ListState.departments,
                    lambda department: rx.table.row(
                        rx.table.cell(department.nombre),
                        rx.table.cell(
                        edit_department_button(department)
                        ),  # Pasamos el objeto department completo
                    ),
                )
            ),
            width="100%",
        ),
        width="100%",
    )
