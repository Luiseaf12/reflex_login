import reflex as rx

from .auth.pages import login_page, logout_page
from .pages import protected_page, info_page
from .user.search import search as user_search
from .search import search
from .navigation import routes
from .ui import (
    logout_item,
    login_item,
    protected_item,
    info_item,
    dark_mode_toggle_item,
)
from .user.list import user_list


app = rx.App()


class TextfieldControlled1(rx.State):
    text: str = "Hello World!"


def controlled_example1():
    return rx.vstack(
        rx.heading(TextfieldControlled1.text),
        rx.input(
            rx.input.slot(
                rx.icon(tag="search"),
            ),
            placeholder="Search here...",
            value=TextfieldControlled1.text,
            on_change=TextfieldControlled1.set_text,
        ),
    )


def index() -> rx.Component:
    return rx.vstack(
        rx.text("Home"),
        login_item(),
        logout_item(),
        protected_item(),
        info_item(),
        user_list(),
        dark_mode_toggle_item(),
        user_search(),
        padding="2em",
    )


app.add_page(index, "/", title="Home")
app.add_page(login_page, routes.LOGIN_ROUTE, title="Login")
app.add_page(
    logout_page,
    route=routes.LOGOUT_ROUTE,
    title="Logout",
)
app.add_page(protected_page, routes.PROTECTED_ROUTE, title="Protected")
app.add_page(info_page, routes.INFO_ROUTE, title="Info")
