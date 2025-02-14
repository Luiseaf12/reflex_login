import reflex as rx
from .local_auth import LocalAuthState
from typing import Optional
from sqlmodel import select, Session

from ..models import UserModel


class SessionState(LocalAuthState):
    @rx.var(cache=True)
    def my_user_id(self) -> int | None:
        if not self.authenticated_user_info:
            return None
        if self.authenticated_user_info.id < 0:
            return None
        return self.authenticated_user_info.id

    @rx.var(cache=True)
    def my_user_id(self) -> int | None:
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.id

    @rx.var(cache=True)
    def authenticated_username(self) -> str | None:
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.username

    @rx.var(cache=True)
    def authenticated_user_info(self) -> UserModel | None:
        if self.authenticated_user.id < 0:
            return None
        with rx.session() as session:
            statement = select(UserModel).where(
                UserModel.id == self.authenticated_user.id
            )
            result = session.exec(statement).one_or_none()
            if result is None:
                return None
            return result

    def on_load(self):
        if not self.is_authenticated:
            return LoginState.redir

    def perform_logout(self):
        self.do_logout()
        return rx.redirect("/")
