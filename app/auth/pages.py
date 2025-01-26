"""An example login page that can be used as-is."""

import reflex as rx

from .login import LoginState
from .state import SessionState
from .components import input_100w, MIN_WIDTH, PADDING_TOP


def login_error() -> rx.Component:
    """Render the login error message."""
    return rx.cond(
        LoginState.error_message != "",
        rx.callout(
            LoginState.error_message,
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            width="100%",
        ),
    )


def login_form() -> rx.Component:
    """Render the login form."""
    return rx.form(
        rx.vstack(
            rx.heading("Login into your Account", size="7"),
            login_error(),
            rx.text("Username"),
            input_100w("username"),
            rx.text("Password"),
            input_100w("password", type="password"),
            rx.button("Sign in", width="100%"),
            min_width=MIN_WIDTH,
        ),
        on_submit=LoginState.on_submit,
    )


def login_page() -> rx.Component:
    """Render the login page.

    Returns:
        A reflex component.
    """
    return rx.center(
        rx.cond(
            LoginState.is_hydrated,  # type: ignore
            rx.card(login_form()),
        ),
        padding_top=PADDING_TOP,
    )


def logout_page() -> rx.Component:
    # Welcome Page (Index)
    my_child = rx.vstack(
        rx.heading("Are you sure?", size="7"),
        rx.hstack(
            rx.button(
                "No, stay logged in", color_scheme="gray", on_click=rx.redirect("/")
            ),
            rx.button(
                "yes logout", on_click=SessionState.perform_logout, color_scheme="red"
            ),
        ),
        spacing="5",
        justify="center",
        text_align="center",
        min_height="85vh",
        id="my-child",
    )
    return my_child
