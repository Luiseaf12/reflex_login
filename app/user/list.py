import reflex as rx

from .state import UserState, ListState
from .forms import create_user_form


def user_list() -> rx.Component:
    """Render the list of available users."""
    return rx.vstack(
        rx.hstack(
            rx.heading("Usuarios Disponibles", size="6"),
            rx.button(
                "Nuevo Usuario",
                on_click=UserState.toggle_form,
                color_scheme="blue",
            ),
            width="100%",
            justify="between",
        ),
        create_user_form(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Username"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Estado"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    ListState.users,
                    lambda user: rx.table.row(
                        rx.table.cell(user.username),
                        rx.table.cell(user.email),
                        rx.table.cell(rx.cond(user.enabled, "Activo", "Inactivo")),
                    ),
                )
            ),
            width="100%",
        ),
        width="100%",
    )
