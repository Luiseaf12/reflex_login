"""An example login page that can be used as-is."""

import reflex as rx

from .login import LoginState
from .state import SessionState
from .registration import RegistrationState
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


def register_error() -> rx.Component:
    """Render the registration error message."""
    return rx.cond(
        RegistrationState.error_message != "",
        rx.callout(
            RegistrationState.error_message,
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            width="100%",
        ),
    )


def register_form() -> rx.Component:
    """Render the registration form."""
    return rx.form(
        rx.vstack(
            rx.heading("Create an account", size="7"),
            register_error(),
            rx.text("Username"),
            input_100w("username"),
            rx.text("Email"),
            input_100w("email", type="email"),
            rx.text("Password"),
            input_100w("password", type="password"),
            rx.text("Confirm Password"),
            input_100w("confirm_password", type="password"),
            rx.button("Sign up", width="100%"),
            rx.center(
                rx.link("Login", on_click=lambda: rx.redirect("/login")),
                width="100%",
            ),
            min_width=MIN_WIDTH,
        ),
        on_submit=RegistrationState.handle_registration,
    )


def registration_page() -> rx.Component:
    """Render the registration page.

    Returns:
        A reflex component.
    """

    return rx.center(
        rx.cond(
            RegistrationState.success,
            rx.vstack(
                rx.text("Registration successful!"),
            ),
            rx.card(register_form()),
        ),
        padding_top=PADDING_TOP,
    )
