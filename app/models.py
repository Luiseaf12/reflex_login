#from __future__ import annotations

import bcrypt
#import sqlalchemy
from sqlmodel import Field, Relationship
from typing import Optional, List

import reflex as rx


class DepartmentModel(
    rx.Model,
    table=True,  # type: ignore
):
    """Modelo para departamentos."""
    
    nombre: str = Field(unique=True, nullable=False, index=True)
    users: List['UserModel'] = Relationship(back_populates="department")

    def dict(self, *args, **kwargs) -> dict:
        """Return a dictionary representation of the department."""
        d = super().dict(*args, **kwargs)
        # Evitamos ciclos infinitos en la serialización
        d.pop("users", None)
        # Solo incluimos los campos básicos
        return {
            "id": d.get("id"),
            "nombre": d.get("nombre")
        }


class UserModel(
    rx.Model,
    table=True,  # type: ignore
):
    """A local User model with bcrypt password hashing."""

    username: str = Field(unique=True, nullable=False, index=True)
    password_hash: bytes = Field(nullable=False)
    enabled: bool = False
    email: str
    
    # Relación con departamento
    department_id: Optional[int] = Field(default=None, foreign_key="departmentmodel.id",sa_column_kwargs={"name": "fk_user_department"})
    department: Optional[DepartmentModel] = Relationship(back_populates="users")

    @staticmethod
    def hash_password(secret: str) -> str:
        """Hash the secret using bcrypt.

        Args:
            secret: The password to hash.

        Returns:
            The hashed password.
        """
        return bcrypt.hashpw(
            password=secret.encode("utf-8"),
            salt=bcrypt.gensalt(),
        )

    def verify(self, secret: str) -> bool:
        """Validate the user's password.

        Args:
            secret: The password to check.

        Returns:
            True if the hashed secret matches this user's password_hash.
        """
        return bcrypt.checkpw(
            password=secret.encode("utf-8"),
            hashed_password=self.password_hash,
        )

    def dict(self, *args, **kwargs) -> dict:
        """Return a dictionary representation of the user."""
        d = super().dict(*args, **kwargs)
        # Never return the hash when serializing to the frontend.
        d.pop("password_hash", None)
        # Include department name if available
        try:
            if hasattr(self, "_sa_instance_state"):
                # Si el objeto está cargado en la sesión y tiene department
                if self._sa_instance_state.committed_state.get("department") is not None:
                    d["department_name"] = self.department.nombre if self.department else None
        except Exception:
            # Si hay algún error al acceder a department, simplemente no lo incluimos
            pass
        return d
