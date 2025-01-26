import reflex as rx
from ..ui import form_field
from .state import UserState


# Atoms (Átomos)
def error_message(message: str) -> rx.Component:
    """Átomo para mostrar mensajes de error."""
    return rx.text(
        message,
        color="red",
        font_size="sm",
    )


def action_button(text: str, on_click, color_scheme: str) -> rx.Component:
    """Átomo para botones de acción."""
    return rx.button(
        text,
        on_click=on_click,
        color_scheme=color_scheme,
    )


# Molecules (Moléculas)
def user_form_fields() -> rx.Component:
    """Molécula que agrupa los campos del formulario."""
    return rx.vstack(
        form_field(
            "Usuario",
            "Nombre de usuario",
            "text",
            "username",
            "user",
            UserState.username,
        ),
        form_field(
            "Contraseña",
            "********",
            "password",
            "password",
            "lock",
            UserState.password,
        ),
        form_field(
            "Email",
            "usuario@dominio.com",
            "email",
            "email",
            "mail",
            UserState.email,
        ),
        spacing="3",
    )


def form_actions() -> rx.Component:
    """Molécula que agrupa los botones de acción."""
    return rx.hstack(
        action_button("Cancelar", UserState.toggle_form, "red"),
        action_button("Crear Usuario", UserState.create_user, "green"),
        spacing="3",
    )


# Organisms (Organismos)
def create_user_form() -> rx.Component:
    """Organismo que representa el formulario completo de creación de usuario."""
    return rx.cond(
        UserState.show_form,
        rx.vstack(
            rx.heading("Crear Usuario", size="4"),
            user_form_fields(),
            error_message(UserState.error_message),
            form_actions(),
            padding="1em",
            border="1px solid #eaeaea",
            border_radius="0.5em",
            spacing="4",
        ),
    )
