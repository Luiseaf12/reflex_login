import reflex as rx
from sqlmodel import select
from typing import List

from ..auth.user import LocalUser


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
