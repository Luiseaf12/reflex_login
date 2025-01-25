"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx


from .auth.pages import login_page
from .auth.login import LoginState

from .navigation import routes


app = rx.App()


def user_list() -> rx.Component:
    """Render the list of available users."""
    return rx.vstack(
        rx.heading("Usuarios Disponibles", size="6"),
        rx.table.root(
            rx.table.column_header_cell("username", width="35%"),
            pagination=True,
            search=True,
            data=LoginState.user_list,
        ),
        width="100%",
    )


def index() -> rx.Component:
    return rx.vstack(
        rx.text("Hello worldddddddddddd!"),
        user_list(),
    )


app.add_page(index, route=routes.HOME_ROUTE, title="Home")
app.add_page(login_page, route=routes.LOGIN_ROUTE, title="Login")
