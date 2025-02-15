import reflex as rx
from ..ui.form_field import form_field
from .state import ListState
from .add import add_user_button
from .edit import edit_user_button
from .search_user import search_dialog as search_user


def user_list() -> rx.Component:
    """Template que representa la lista completa de usuarios."""
    return rx.vstack(
        rx.hstack(
            rx.heading("Usuarios Disponibles", size="6"),
            width="100%",
            justify="between",
        ),
        add_user_button(),
        #search_user(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Username"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Departamento"),
                    rx.table.column_header_cell("Estado"),
                    rx.table.column_header_cell("Acciones"),
                )
            ),
            rx.table.body(
                rx.cond(
                    ListState.has_users,
                    rx.foreach(
                        ListState.users,
                        lambda user: rx.table.row(
                            rx.table.cell(user.username),
                            rx.table.cell(user.email),
                            rx.table.cell(user.department_id),
                            rx.table.cell(rx.cond(user.enabled, "Activo", "Inactivo")),
                            rx.table.cell(
                                edit_user_button(user)
                            ),
                        ),
                    ),
                    rx.table.row(
                        rx.table.cell(
                            rx.text("No hay usuarios registrados", color="gray"),
                            colspan=5,
                            text_align="center",
                        )
                    ),
                )
            ),
            width="100%",
        ),
        width="100%",
        on_mount=ListState.on_mount,
    )
