import reflex as rx
from ..ui.form_field import form_field
from .state import ListState
from .add import add_user_button
from .edit import edit_user_button


def user_list() -> rx.Component:
    """Template que representa la lista completa de usuarios."""
    return rx.vstack(
        rx.hstack(
            rx.heading("Usuarios Disponibles", size="6"),
            width="100%",
            justify="between",
        ),
        add_user_button(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Username"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Estado"),
                    rx.table.column_header_cell("Acciones"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    ListState.users,
                    lambda user: rx.table.row(
                        rx.table.cell(user.username),
                        rx.table.cell(user.email),
                        rx.table.cell(rx.cond(user.enabled, "Activo", "Inactivo")),
                        rx.table.cell(
                            edit_user_button(user)
                        ),  # Pasamos el objeto user completo
                    ),
                )
            ),
            width="100%",
        ),
        width="100%",
    )
