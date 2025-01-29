import reflex as rx
from sqlmodel import select
from typing import List, Optional, Union, Dict, Any

from ..auth.model import LocalUser


class UserState(rx.State):
    """State for user management."""

    username: str = ""
    password: str = ""
    email: str = ""
    show_form: bool = False
    error_message: str = ""
    edit_mode: bool = False
    user_id: Optional[int] = None

    def toggle_form(self):
        """Toggle the form visibility."""
        if self.show_form:
            self.clear_form()
        else:
            self.show_form = True

    def clear_form(self):
        """Clear the form fields."""
        self.username = ""
        self.password = ""
        self.email = ""
        self.error_message = ""
        self.show_form = False
        self.edit_mode = False
        self.user_id = None

    def set_edit_user(self, user: Any):
        """Set user data for editing."""
        try:
            # Extraer el ID del usuario
            user_id = (
                user.get("id") if isinstance(user, dict) else getattr(user, "id", None)
            )

            if not user_id:
                self.error_message = "Error: ID de usuario no válido"
                return

            # Buscar el usuario en la base de datos
            with rx.session() as session:
                db_user = session.get(LocalUser, user_id)
                if not db_user:
                    self.error_message = "Usuario no encontrado"
                    return

                # Actualizar el estado con los datos del usuario
                self.user_id = db_user.id
                self.username = db_user.username
                self.email = db_user.email
                self.password = ""  # No mostrar contraseña actual
                self.edit_mode = True
                self.show_form = True
                self.error_message = ""

        except Exception as e:
            self.error_message = f"Error al cargar usuario: {str(e)}"
            self.clear_form()

    def create_user(self, form_data: dict):
        """Create a new user from form data."""
        # Extract form data
        self.username = form_data.get("username", "")
        self.password = form_data.get("password", "")
        self.email = form_data.get("email", "")

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
            session.refresh(new_user)

            # Clear form and close dialog only on success
            self.clear_form()

    def update_user(self, form_data: dict):
        """Update existing user from form data."""
        if not self.user_id:
            self.error_message = "Error: Usuario no encontrado"
            return

        self.username = form_data.get("username", "")
        self.email = form_data.get("email", "")
        password = form_data.get("password", "")

        if not self.username or not self.email:
            self.error_message = "Username y email son requeridos"
            return

        with rx.session() as session:
            # Get user to update
            user = session.get(LocalUser, self.user_id)
            if not user:
                self.error_message = "Usuario no encontrado"
                return

            # Check if new username is already taken by another user
            existing_user = session.exec(
                select(LocalUser).where(
                    LocalUser.username == self.username, LocalUser.id != self.user_id
                )
            ).first()

            if existing_user:
                self.error_message = "El nombre de usuario ya existe"
                return

            # Update user data
            user.username = self.username
            user.email = self.email
            if password:  # Solo actualizar contraseña si se proporciona una nueva
                user.password_hash = LocalUser.hash_password(password)

            session.add(user)
            session.commit()

            # Clear form and close dialog only on success
            self.clear_form()

    def set_username(self, username: str):
        """Set username field."""
        self.username = username
        self.error_message = ""

    def set_password(self, password: str):
        """Set password field."""
        self.password = password
        self.error_message = ""

    def set_email(self, email: str):
        """Set email field."""
        self.email = email
        self.error_message = ""


class ListState(rx.State):
    """State for user listing."""

    @rx.var(cache=False)
    def users(self) -> List[LocalUser]:
        """Get all users from database."""
        with rx.session() as session:
            statement = select(LocalUser)
            return session.exec(statement).all()
