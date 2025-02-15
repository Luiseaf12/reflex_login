import reflex as rx
from sqlmodel import select
from typing import List, Optional, Union, Dict, Any

from ..models import DepartmentModel


class DepartamentState(rx.State):
    """State for department management."""

    nombre: str = ""
    show_add_form: bool = False  # Para el diálogo de agregar
    show_edit_form: bool = False  # Para el diálogo de editar
    error_message: str = ""
    edit_mode: bool = False
    department_id: Optional[int] = None

    # def toggle_add_form(self):
    #     """Toggle the add form visibility."""
    #     if self.show_add_form:
    #         self.clear_form()
    #     else:
    #         self.show_add_form = True
    #         self.show_edit_form = False  # Aseguramos que el otro diálogo esté cerrado
    
    def toggle_add_form(self):
        """Abre/cierra el formulario y resetea el buscador."""
        self.show_add_form = not self.show_add_form
        if not self.show_add_form:
            SearchDepartamentState.reset_selection()  # Resetear al cerrar

    def toggle_edit_form(self):
        """Toggle the edit form visibility."""
        if self.show_edit_form:
            self.clear_form()
        else:
            self.show_edit_form = True
            self.show_add_form = False  # Aseguramos que el otro diálogo esté cerrado

    def clear_form(self):
        """Clear the form fields."""
        try:
            self.nombre = ""
            self.error_message = ""
            self.show_add_form = False
            self.show_edit_form = False
            self.edit_mode = False
            self.department_id = None
        except Exception as e:
            self.error_message = f"Error al limpiar el formulario: {str(e)}"

    def set_edit_department(self, department: Any):
        """Set department data for editing."""
        try:
            # Extraer el ID del departamento
            department_id = (
                department.get("id") if isinstance(department, dict) else getattr(department, "id", None)
            )

            if not department_id:
                self.error_message = "Error: ID de departamento no válido"
                return

            # Buscar el departamento en la base de datos
            with rx.session() as session:
                db_department = session.get(DepartmentModel, department_id)
                if not db_department:
                    self.error_message = "Departamento no encontrado"
                    return

                # Actualizar el estado con los datos del departamento
                self.department_id = db_department.id
                self.nombre = db_department.nombre
                self.edit_mode = True
                self.show_edit_form = True
                self.error_message = ""

        except Exception as e:
            self.error_message = f"Error al cargar departamento: {str(e)}"
            self.clear_form()

    def create_department(self, form_data: dict):
        """Create a new department from form data."""
        # Extract form data
        self.nombre = form_data.get("nombre", "")

        if not self.nombre:
            self.error_message = "Todos los campos son requeridos"
            return

        with rx.session() as session:
            # Check if nombre already exists
            existing_department = session.exec(
                select(DepartmentModel).where(DepartmentModel.nombre == self.nombre)
            ).first()

            if existing_department:
                self.error_message = "El nombre de departamento ya existe"
                return

            # Create new department
            new_department = DepartmentModel(
                nombre=self.nombre,
            )
            session.add(new_department)
            session.commit()
            session.refresh(new_department)

            # Clear form and close dialog only on success
            self.clear_form()

    def update_department(self, form_data: dict):
        """Update existing department from form data."""
        if not self.department_id:
            self.error_message = "Error: Departamento no encontrado"
            return

        # Obtener los valores del formulario
        nombre = form_data.get("nombre", self.nombre).strip()

        if not nombre:
            self.error_message = "nombre es requerido"
            return

        try:
            with rx.session() as session:
                # Get department to update
                department = session.get(DepartmentModel, self.department_id)
                if not department:
                    self.error_message = "Departamento no encontrado"
                    return

                # Check if new nombre is already taken by another department
                if nombre != department.nombre:  # Solo verificar si el nombre cambió
                    existing_department = session.exec(
                        select(DepartmentModel).where(
                            DepartmentModel.nombre == nombre, 
                            DepartmentModel.id != self.department_id
                        )
                    ).first()

                    if existing_department:
                        self.error_message = "El nombre de departamento ya existe"
                        return

                # Update department data
                department.nombre = nombre
                session.add(department)
                session.commit()

                # Clear form and close dialog only on success
                self.clear_form()
        except Exception as e:
            self.error_message = f"Error al actualizar departamento: {str(e)}"

    def set_nombre(self, nombre: str):
        """Set nombre field."""
        self.nombre = nombre
        self.error_message = ""

class ListState(rx.State):
    """State for department listing."""

    @rx.var(cache=False)
    def departments(self) -> List[DepartmentModel]:
        """Get all departments from database."""
        with rx.session() as session:
            statement = select(DepartmentModel)
            return session.exec(statement).all()
