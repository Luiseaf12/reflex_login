import reflex as rx
from ..ui.form_field import form_field
from .state import UserState


# Atoms (Átomos)
def icon_button(icon: str, text: str, size: str = "3") -> rx.Component:
    """Átomo para botón con icono."""
    return rx.button(
        rx.icon(icon, size=26),
        rx.text(text, size="4", display=["none", "none", "block"]),
        size=size,
    )


def badge_icon(icon: str, size: int = 34) -> rx.Component:
    """Átomo para badge con icono."""
    return rx.badge(
        rx.icon(tag=icon, size=size),
        color_scheme="grass",
        radius="full",
        padding="0.65rem",
    )


# Molecules (Moléculas)
def dialog_header() -> rx.Component:
    """Molécula para el encabezado del diálogo."""
    return rx.hstack(
        badge_icon("users"),
        rx.vstack(
            rx.dialog.title(
                "Agregar usuario",
                weight="bold",
                margin="0",
            ),
            rx.dialog.description(
                "Llena el formulario con la información del usuario",
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


def user_form_fields() -> rx.Component:
    """Molécula que agrupa los campos del formulario."""
    return rx.flex(
        rx.form.field(
            rx.flex(
                rx.hstack(
                    rx.icon("user", size=16, stroke_width=1.5),
                    rx.form.label("Usuario"),
                    rx.text("*", color="red"),
                    align="center",
                    spacing="2",
                ),
                rx.input(
                    placeholder="Nombre de usuario",
                    id="username",
                    name="username",
                    required=True,
                ),
                direction="column",
                spacing="1",
            ),
            name="username",
        ),
        rx.form.field(
            rx.flex(
                rx.hstack(
                    rx.icon("lock", size=16, stroke_width=1.5),
                    rx.form.label("Contraseña"),
                    rx.text("*", color="red"),
                    align="center",
                    spacing="2",
                ),
                rx.input(
                    placeholder="********",
                    type="password",
                    id="password",
                    name="password",
                    required=True,
                ),
                direction="column",
                spacing="1",
            ),
            name="password",
        ),
        rx.form.field(
            rx.flex(
                rx.hstack(
                    rx.icon("mail", size=16, stroke_width=1.5),
                    rx.form.label("Email"),
                    rx.text("*", color="red"),
                    align="center",
                    spacing="2",
                ),
                rx.input(
                    placeholder="usuario@dominio.com",
                    type="email",
                    id="email",
                    name="email",
                    required=True,
                ),
                direction="column",
                spacing="1",
            ),
            name="email",
        ),
        direction="column",
        spacing="3",
    )


def form_actions() -> rx.Component:
    """Molécula para los botones de acción."""
    return rx.flex(
        rx.button(
            "Cancelar",
            variant="soft",
            color_scheme="gray",
            type="button",
            on_click=UserState.clear_form,
        ),
        rx.button(
            "Crear Usuario",
            type="submit",
            color_scheme="grass",
        ),
        padding_top="2em",
        spacing="3",
        mt="4",
        justify="end",
    )


# Organisms (Organismos)
def user_form() -> rx.Component:
    """Organismo que representa el formulario de usuario."""
    return rx.form.root(
        rx.flex(
            user_form_fields(),
            rx.text(
                UserState.error_message,
                color="red",
                size="4",
            ),
            form_actions(),
            direction="column",
            spacing="4",
        ),
        on_submit=UserState.create_user,
        reset_on_submit=False,
    )


def add_user_button() -> rx.Component:
    """Organismo que representa el diálogo completo para agregar usuario."""
    return rx.dialog.root(
        rx.dialog.trigger(
            icon_button("users", "Agregar Usuario"),
            on_click=UserState.toggle_add_form,
        ),
        rx.dialog.content(
            dialog_header(),
            rx.flex(
                user_form(),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
        open=UserState.show_add_form,
    )
