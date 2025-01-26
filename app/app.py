import reflex as rx

from .auth.pages import login_page, logout_page
from .pages import protected_page
from .navigation import routes
from .ui import logout_item, login_item, protected_item
from .user.list import user_list


app = rx.App()


def index() -> rx.Component:
    return rx.vstack(
        rx.text("Home"),
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
app.add_page(protected_page, routes.PROTECTED_ROUTE, title="Protected")
