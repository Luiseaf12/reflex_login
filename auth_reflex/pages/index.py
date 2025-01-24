import reflex as rx
from ..auth.list import users_table_component
from ..auth.state import UsersState

@rx.page("/", title="Home")
def index_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Bienvenido a Auth Reflex", font_size="2em"),
            rx.hstack(
                rx.link(
                    rx.button(
                        "Iniciar Sesión",
                        size="4",
                    ),
                    href="/login",
                ),
            ),
            rx.heading("Usuarios Registrados", font_size="1.5em", margin_top="2em"),
            users_table_component(),
            spacing="4",
            width="80%",
            padding_top="5%",
        ),
    )