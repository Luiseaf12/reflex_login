"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from sqlmodel import select
from typing import List

from .auth.pages import login_page, logout_page
from .auth.login import LoginState
from .auth.user import LocalUser
from .navigation import routes, NavState
from .protected import protected_page

from .user.forms import user_list


class UserState(rx.State):
    """State for user management."""

    username: str = ""
    password: str = ""
    email: str = ""
    show_form: bool = False
    error_message: str = ""

    def toggle_form(self):
        """Toggle the form visibility."""
        self.show_form = not self.show_form
        self.clear_form()

    def clear_form(self):
        """Clear the form fields."""
        self.username = ""
        self.password = ""
        self.email = ""
        self.error_message = ""

    def create_user(self):
        """Create a new user."""
        if not self.username or not self.password or not self.email:
            self.error_message = "Todos los campos son requeridos"
            return

        with rx.session() as session:
            # Check if username already exists
            existing_user = session.exec(
                select(LocalUser).where(LocalUser.username == self.username)
            ).first()

            if existing_user:
                self.error_message = "El nombre de usuario ya existe"
                return

            # Create new user
            new_user = LocalUser(
                username=self.username,
                password_hash=LocalUser.hash_password(self.password),
                email=self.email,
                enabled=True,
            )
            session.add(new_user)
            session.commit()

        self.toggle_form()


class ListState(rx.State):
    """State for user listing."""

    @rx.var(cache=False)
    def users(self) -> List[LocalUser]:
        """Get all users from database."""
        with rx.session() as session:
            statement = select(LocalUser)
            return session.exec(statement).all()


app = rx.App()


def create_user_form() -> rx.Component:
    """Render the create user form."""
    return rx.cond(
        UserState.show_form,
        rx.vstack(
            rx.heading("Crear Usuario", size="4"),
            rx.input(
                placeholder="Username",
                value=UserState.username,
                on_change=UserState.set_username,
            ),
            rx.input(
                type_="password",
                placeholder="Password",
                value=UserState.password,
                on_change=UserState.set_password,
            ),
            rx.input(
                type_="email",
                placeholder="Email",
                value=UserState.email,
                on_change=UserState.set_email,
            ),
            rx.text(
                UserState.error_message,
                color="red",
                font_size="sm",
            ),
            rx.hstack(
                rx.button(
                    "Cancelar",
                    on_click=UserState.toggle_form,
                    color_scheme="red",
                ),
                rx.button(
                    "Crear Usuario",
                    on_click=UserState.create_user,
                    color_scheme="green",
                ),
            ),
            padding="1em",
            border="1px solid #eaeaea",
            border_radius="0.5em",
        ),
    )


def user_listxx() -> rx.Component:
    """Render the list of available users."""
    return rx.vstack(
        rx.hstack(
            rx.heading("Usuarios Disponibles", size="6"),
            rx.button(
                "Nuevo Usuario",
                on_click=UserState.toggle_form,
                color_scheme="blue",
            ),
            width="100%",
            justify="between",
        ),
        create_user_form(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Username"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Estado"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    ListState.users,
                    lambda user: rx.table.row(
                        rx.table.cell(user.username),
                        rx.table.cell(user.email),
                        rx.table.cell(rx.cond(user.enabled, "Activo", "Inactivo")),
                    ),
                )
            ),
            width="100%",
        ),
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


def index() -> rx.Component:
    return rx.vstack(
        rx.text("Hello world!"),
        login_item(),
        logout_item(),
        protected_item(),
        user_list(),
        padding="2em",
    )


app.add_page(index, "/", title="Home")
app.add_page(login_page, routes.LOGIN_ROUTE, title="Login")
app.add_page(
    logout_page,
    route=routes.LOGOUT_ROUTE,
    title="Logout",
)
app.add_page(protected_page, "/protected", title="Protected")
