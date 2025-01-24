"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx

from .auth.state import SessionState
from .auth.pages import login_page
from . import pages
from .navigation import routes




app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        panel_background="solid" ,
        radius="medium",
        accent_color="sky" ,
        scaling ="95%",  
        )
    )

app.add_page(pages.index_page, route=routes.HOME_ROUTE, title="Home")
app.add_page(login_page, route=routes.LOGIN_ROUTE, title="Login")
