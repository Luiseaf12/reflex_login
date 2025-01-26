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
                rx.text("*", color="red") if required else None,
                align="center",
                spacing="2",
            ),
            rx.form.control(
                rx.input(
                    placeholder=placeholder,
                    type=type,
                    value=value,
                    on_change=on_change,
                    required=required,
                ),
                as_child=True,
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )
