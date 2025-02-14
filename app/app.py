import reflex as rx

from .auth.pages import login_page, logout_page, registration_page
from .pages import protected_page, info_page, contact_page
from .navigation import routes
from .ui import (
    logout_item,
    login_item,
    registration_item,
    protected_item,
    info_item,
    dark_mode_toggle_item,
    contact_item,
)
from .user.list import user_list
from .department.list import department_list

app = rx.App()





def index() -> rx.Component:
    return rx.vstack(
        rx.text("Home"),
        login_item(),
        logout_item(),
        registration_item(),
        protected_item(),
        info_item(),
        contact_item(),
        user_list(),
        dark_mode_toggle_item(),
        department_list(),
        padding="2em",
    )


app.add_page(index, "/", title="Home")
app.add_page(login_page, routes.LOGIN_ROUTE, title="Login")
app.add_page(
    logout_page,
    route=routes.LOGOUT_ROUTE,
    title="Logout",
)
app.add_page(contact_page, routes.CONTACT_ROUTE, title="Contact")
app.add_page(protected_page, routes.PROTECTED_ROUTE, title="Protected")
app.add_page(info_page, routes.INFO_ROUTE, title="Info")
app.add_page(registration_page, routes.REGISTRATION_ROUTE, title="Registration")
