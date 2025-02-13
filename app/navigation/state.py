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

    def to_info(self):
        return rx.redirect(routes.INFO_ROUTE)

    def to_contact(self):
        return rx.redirect(routes.CONTACT_ROUTE)

    def to_registration(self):
        return rx.redirect(routes.REGISTRATION_ROUTE)

    def to_protected(self):
        return rx.redirect(routes.PROTECTED_ROUTE)
