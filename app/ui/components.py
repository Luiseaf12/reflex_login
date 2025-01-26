import reflex as rx

from ..navigation import NavState


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


def logout_item() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("log-out"),
            rx.text("Log out", size="4"),
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
        on_click=NavState.to_logout,
        as_="button",
        width="100%",
    )


def login_item() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("log-in"),
            rx.text("Login", size="4"),
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
        on_click=NavState.to_login,
        as_="button",
        width="100%",
    )


def protected_item() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("shield-check"),
            rx.text("pagina protegida", size="4"),
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
        on_click=NavState.to_protected,
        as_="button",
        width="100%",
    )


def info_item() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("info"),
            rx.text("Info", size="4"),
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
        on_click=NavState.to_info,
        as_="button",
        width="100%",
    )
