import reflex as rx
from ..ui.form_field import form_field
from .state import UserState


# Atoms (Átomos)
def badge_icon(icon: str, size: int = 34) -> rx.Component:
    """Átomo para badge con icono."""
    return rx.badge(
        rx.icon(tag=icon, size=size),
        color_scheme="grass",
        radius="full",
        padding="0.65rem",
    )
 

# Molecules (Moléculas)
def edit_dialog_header() -> rx.Component:
    """Molécula para el encabezado del diálogo de edición."""
    return rx.hstack(
        badge_icon("pencil"),
        rx.vstack(
            rx.dialog.title(
                "Editar usuario",
                weight="bold",
                margin="0",
            ),
            rx.dialog.description(
                "Modifica la información del usuario",
            ),
            spacing="1",
            height="100%",
            align_items="start",
        ),
        height="100%",
        spacing="4",
        margin_bottom="1.5em",
        align_items="center",
        width="100%",
    )


def edit_form_fields() -> rx.Component:
    """Molécula que agrupa los campos del formulario de edición."""
    return rx.flex(
        form_field(
            "Usuario",
            "Nombre de usuario",
            "text",
            "username",
            "user",
            value=UserState.username,
            on_change=UserState.set_username,
            required=True,
        ),
        form_field(
            "Contraseña",
            "Dejar vacío para mantener la actual",
            "password",
            "password",
            "lock",
            value=UserState.password,
            on_change=UserState.set_password,
            required=False,
        ),
        form_field(
            "Email",
            "usuario@dominio.com",
            "email",
            "email",
            "mail",
            value=UserState.email,
            on_change=UserState.set_email,
            required=True,
        ),
        direction="column",
        spacing="3",
    )


def edit_form_actions() -> rx.Component:
    """Molécula para los botones de acción de edición."""
    return rx.flex(
        rx.dialog.close(
            rx.button(
                "Cancelar",
                variant="soft",
                color_scheme="gray",
                on_click=UserState.clear_form,
            ),
        ),
        rx.button(
            "Guardar Cambios",
            type="submit",
            color_scheme="grass",
        ),
        padding_top="2em",
        spacing="3",
        mt="4",
        justify="end",
    )


# Organisms (Organismos)
def edit_user_form() -> rx.Component:
    """Organismo que representa el formulario de edición de usuario."""
    return rx.form.root(
        rx.flex(
            edit_form_fields(),
            rx.text(
                UserState.error_message,
                color="red",
                size="4",
            ),
            edit_form_actions(),
            direction="column",
            spacing="4",
        ),
        on_submit=UserState.update_user,
        reset_on_submit=False,
    )


def edit_user_button(user: dict) -> rx.Component:
    """Átomo para botón de edición de usuario."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("pencil", size=20),
                size="1",
                variant="soft",
                on_click=lambda: UserState.set_edit_user(user),
            ),
        ),
        rx.dialog.content(
            edit_dialog_header(),
            rx.flex(
                edit_user_form(),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
        open=UserState.show_edit_form,  # Usamos el nuevo estado
    )
