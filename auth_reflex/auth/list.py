import reflex as rx
from typing import List
from ..models import User
from .state import UsersState

# Atoms (Componentes básicos)
def table_header_cell(text: str) -> rx.Component:
    """Crear una celda de encabezado de tabla."""
    return rx.table.column(text)

def action_button(text: str, color_scheme: str) -> rx.Component:
    """Crear un botón de acción."""
    return rx.button(
        text,
        color_scheme=color_scheme,
        size="2"
    )

def table_header() -> rx.Component:
    return rx.table.header(
        rx.table.row(
            rx.table.column_header_cell("ID", width="5%", text_align="center"),
            rx.table.column_header_cell("Usuario", width="25%"),
        ),
        bg="gray.900",
    )

def table_row(item: User) -> rx.Component:
    return rx.table.row(
        rx.table.cell(item.id, text_align="center"),
        rx.table.cell(item.username),
        cursor="pointer",
        _hover={"bg": "gray.700"},
    )

   
def users_table_component() -> rx.Component:
    return rx.box(
        rx.table.root(
            table_header(),
            rx.table.body(
                rx.cond(
                    UsersState.users,
                    rx.foreach(
                        UsersState.users,
                        table_row,
                    ),
                    rx.table.row(
                        rx.table.cell(
                            "No hay usuarios disponibles",
                            colspan=2,
                            text_align="center",
                            color="gray.500",
                            font_style="italic",
                        ),
                    ),
                ),
            ),
            variant="surface",
            size="2",
        ),
        border="1px solid",
        border_color="gray.700",
        border_radius="md",
        overflow="hidden",
    )
