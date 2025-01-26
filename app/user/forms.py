import reflex as rx

from .state import UserState


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
