import reflex as rx
from ..ui.form_field import form_field
from .state import DepartamentState
from .search_department import SearchDepartamentState


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
        badge_icon("activity"),
        rx.vstack(
            rx.dialog.title(
                "Agregar departamento",
                weight="bold",
                margin="0",
            ),
            rx.dialog.description(
                "Llena el formulario con la información del departamento",
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


def department_form_fields() -> rx.Component:
    """Molécula que agrupa los campos del formulario."""
    return rx.flex(
        rx.form.field(
            rx.flex(
                rx.hstack(
                    rx.icon("activity", size=16, stroke_width=1.5),
                    rx.form.label("Departamento"),
                    rx.text("*", color="red"),
                    align="center",
                    spacing="2",
                ),
                rx.input(
                    placeholder="Nombre de departamento",
                    id="nombre",
                    name="nombre",
                    required=True,
                ),
                direction="column",
                spacing="1",
            ),
            name="nombre",
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
            on_click=DepartamentState.clear_form,
        ),
        rx.button(
            "Crear Departamento",
            type="submit",
            color_scheme="grass",
        ),
        padding_top="2em",
        spacing="3",
        mt="4",
        justify="end",
    )


# Organisms (Organismos)
def department_form() -> rx.Component:
    """Organismo que representa el formulario de departamento."""
    return rx.form.root(
        rx.flex(
            department_form_fields(),
            rx.text(
                DepartamentState.error_message,
                color="red",
                size="4",
            ),
            form_actions(),
            direction="column",
            spacing="4",
        ),
        on_submit=DepartamentState.create_department,
        reset_on_submit=False,
    )


def add_department_button() -> rx.Component:
    """Organismo que representa el diálogo completo para agregar departamento."""
    return rx.dialog.root(
        rx.dialog.trigger(
            icon_button("activity", "Agregar Departamento"),
            on_click=DepartamentState.toggle_add_form,
        ),
        rx.dialog.content(
            dialog_header(),
            rx.flex(
                department_form(),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
            on_open_change=SearchDepartamentState.reset_selection,
        ),
        open=DepartamentState.show_add_form,
    )
