import reflex as rx
from sqlmodel import select
from sqlalchemy.orm import joinedload
from typing import List, Optional, Union, Dict, Any
from ..models import UserModel


class UserState(rx.State):
    """State for user management."""

    username: str = ""
    password: str = ""
    email: str = ""
    department_id: Optional[int] = None
    show_add_form: bool = False  # Para el diálogo de agregar
    show_edit_form: bool = False  # Para el diálogo de editar
    error_message: str = ""
    edit_mode: bool = False
    user_id: Optional[int] = None

    def toggle_add_form(self):
        """Toggle the add form visibility."""
        if self.show_add_form:
            self.clear_form()
        else:
            self.show_add_form = True
            self.show_edit_form = False  # Aseguramos que el otro diálogo esté cerrado

    def toggle_edit_form(self):
        """Toggle the edit form visibility."""
        if self.show_edit_form:
            self.clear_form()
        else:
            self.show_edit_form = True
            self.show_add_form = False  # Aseguramos que el otro diálogo esté cerrado

    def clear_form(self):
        """Limpia el formulario y estados relacionados."""
        try:
            # Limpiar campos del formulario
            self.username = ""
            self.password = ""
            self.email = ""
            self.department_id = None
            self.error_message = ""
            
            # Limpiar estados de diálogo
            self.show_add_form = False
            self.show_edit_form = False
            self.edit_mode = False
            self.user_id = None
        except Exception as e:
            self.error_message = f"Error al limpiar el formulario: {str(e)}"



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
                db_user = session.get(UserModel, user_id)
                if not db_user:
                    self.error_message = "Usuario no encontrado"
                    return

                # Actualizar el estado con los datos del usuario
                self.user_id = db_user.id
                self.username = db_user.username
                self.email = db_user.email
                self.password = ""  # No mostrar contraseña actual
                self.department_id = db_user.department_id
                self.edit_mode = True
                self.show_edit_form = True
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
        self.department_id = form_data.get("department_id", None)

        if not self.username or not self.password or not self.email:
            self.error_message = "Todos los campos son requeridos"
            return

        with rx.session() as session:
            # Check if username already exists
            existing_user = session.exec(
                select(UserModel).where(UserModel.username == self.username)
            ).first()

            if existing_user:
                self.error_message = "El nombre de usuario ya existe"
                return

            # Create new user
            new_user = UserModel(
                username=self.username,
                password_hash=UserModel.hash_password(self.password),
                email=self.email,
                enabled=True,
                department_id=self.department_id,
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

        # Obtener los valores del formulario
        username = form_data.get("username", self.username).strip()
        email = form_data.get("email", self.email).strip()
        password = form_data.get("password", "").strip()
        department_id = form_data.get("department_id", self.department_id)

        if not username or not email:
            self.error_message = "Username y email son requeridos"
            return

        try:
            with rx.session() as session:
                # Get user to update
                user = session.get(UserModel, self.user_id)
                if not user:
                    self.error_message = "Usuario no encontrado"
                    return

                # Check if new username is already taken by another user
                if username != user.username:  # Solo verificar si el username cambió
                    existing_user = session.exec(
                        select(UserModel).where(
                            UserModel.username == username, 
                            UserModel.id != self.user_id
                        )
                    ).first()

                    if existing_user:
                        self.error_message = "El nombre de usuario ya existe"
                        return

                # Update user data
                user.username = username
                user.email = email
                if password:  # Solo actualizar contraseña si se proporciona una nueva
                    user.password_hash = UserModel.hash_password(password)
                if department_id:
                    user.department_id = department_id

                session.add(user)
                session.commit()

                # Clear form and close dialog only on success
                self.clear_form()
        except Exception as e:
            self.error_message = f"Error al actualizar usuario: {str(e)}"

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

    def set_department_id(self, value: str):
        """Establece el ID del departamento."""
        try:
            if value and value.strip():
                self.department_id = int(value)
            else:
                self.department_id = None
        except (ValueError, TypeError) as e:
            self.error_message = f"Error al convertir el ID del departamento: {str(e)}"
            self.department_id = None


class ListState(rx.State):
    """State for user listing."""

    users: List[UserModel] = []  # Inicializamos la lista vacía
    has_users: bool = False  # Flag para indicar si hay usuarios

    def on_mount(self):
        """Se ejecuta cuando el componente se monta."""
        self.get_users()

    def get_users(self) -> None:
        """Obtiene todos los usuarios de la base de datos."""
        try:
            with rx.session() as session:
                # Usamos joinedload para cargar la relación department de manera eager
                statement = select(UserModel).options(joinedload(UserModel.department))
                result = session.exec(statement).all()
                self.users = result
                self.has_users = bool(result)
        except Exception as e:
            print(f"Error al obtener usuarios: {str(e)}")
            self.users = []
            self.has_users = False

    def on_load(self):
        """Se ejecuta cuando la página se carga."""
        self.get_users()
