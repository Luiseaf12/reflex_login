import reflex as rx
from typing import Any, Callable, Optional


def form_field(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon: str,
    value: Optional[Any] = None,
    on_change: Optional[Callable] = None,
    required: bool = False,
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.hstack(
                rx.icon(icon, size=16, stroke_width=1.5),
                rx.form.label(label),
                rx.cond(
                    required,
                    rx.text("*", color="red"),
                    rx.text(""),
                ),
                align="center",
                spacing="2",
            ),
            rx.input(
                placeholder=placeholder,
                type=type,
                value=value,
                on_change=on_change,
                required=required,
                name=name,  # Agregamos el name al input
            ),
            direction="column",
            spacing="1",
        ),
        width="100%",
    )
