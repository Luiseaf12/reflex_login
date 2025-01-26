import reflex as rx

from auth_reflex.auth.login import require_login
from .navigation import NavState


def index_item() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("circle-play"),
            rx.text("Inicio", size="4"),
            width="100%",
            paddingX="0.5rem",
            paddingY="0.75rem",
            align="center",
            style={
                "_hover": {
                    "cursor": "pointer",
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "color": rx.color("accent", 11),
                "borderRadius": "0.5em",
            },
        ),
        on_click=NavState.to_home,
        as_="button",
        width="100%",
    )


@require_login
def protected_page() -> rx.Component:
    return rx.vstack(
        rx.text("Pagina protegida"),
        index_item(),
        padding="2em",
    )
