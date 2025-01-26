import reflex as rx

# from sqlmodel import select
# from typing import List

# from .auth.pages import login_page, logout_page
# from .auth.login import LoginState
# from .auth.user import LocalUser
# from .navigation import routes, NavState
# from .protected import protected_page

from .state import UserState, ListState


def create_user_form() -> rx.Component:
    """Render the create user form."""
    return rx.cond(
        UserState.show_form,
        rx.vstack(
            rx.heading("Crear Usuario", size="4"),
            rx.input(
                placeholder="Username",
                value=UserState.username,
                on_change=UserState.set_username,
            ),
            rx.input(
                type_="password",
                placeholder="Password",
                value=UserState.password,
                on_change=UserState.set_password,
            ),
            rx.input(
                type_="email",
                placeholder="Email",
                value=UserState.email,
                on_change=UserState.set_email,
            ),
            rx.text(
                UserState.error_message,
                color="red",
                font_size="sm",
            ),
            rx.hstack(
                rx.button(
                    "Cancelar",
                    on_click=UserState.toggle_form,
                    color_scheme="red",
                ),
                rx.button(
                    "Crear Usuario",
                    on_click=UserState.create_user,
                    color_scheme="green",
                ),
            ),
            padding="1em",
            border="1px solid #eaeaea",
            border_radius="0.5em",
        ),
    )


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
