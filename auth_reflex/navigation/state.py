import reflex as rx
from . import routes
from ..auth.login import LoginState


class NavState(rx.State):
    def to_home(self):
        return rx.redirect(routes.HOME_ROUTE)

    def to_login(self):
        return rx.redirect(routes.LOGIN_ROUTE)

    def to_logout(self):
        return rx.redirect(routes.LOGOUT_ROUTE)
