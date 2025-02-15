import reflex as rx
from typing import List, Type, Optional
from reflex import session
from sqlmodel import select

MODEL_NAME: str = 'UserModel'
SEARCH_PROPERTY: str = "username"
RETURN_PROPERTY: str = "id"
DISPLAY_PROPERTY: str = "username"
ITEM_NAME: str = "usuario"
WIDTH: str = "100%"

class SearchUserState(rx.State):
    """Estado para el buscador dinámico con rx.Model."""
    
    selected_item_id: str = ""
    selected_item_name: str = ""
    show_search_form: bool = False
    search_text: str = ""
    search_results: List[dict] = []
    error_message: str = ""
    input_value: str = ""
    input_error: str = ""
    _model: Type[rx.Model] = None  # Cambiamos a rx.Model
    search_property: str = ""
    return_property: str = "id"
    display_property: str = ""

    def open_search_form(
        self,
        model_name: str,  # Recibir nombre del modelo como string
        search_property: str,
        return_property: str,
        display_property: str
    ):
        """Configura y abre el formulario de búsqueda"""
        try:
            self._model = self.get_model_class(model_name)
            self.search_property = search_property
            self.return_property = return_property
            self.display_property = display_property
            self.show_search_form = True
            self.reset_search()
        except ValueError as e:
            self.error_message = str(e)
            self.show_search_form = False

    def get_model_class(self, model_name: str) -> Type[rx.Model]:
        """Obtiene la clase del modelo por su nombre"""
        for model in rx.Model.__subclasses__():  # Buscar en subclases de rx.Model
            if model.__name__ == model_name:
                return model
        raise ValueError(f"Modelo '{model_name}' no encontrado. Asegúrate de que está importado.")

    def reset_search(self):
        """Reinicia parámetros de búsqueda"""
        self.search_text = ""
        self.search_results = []
        self.error_message = ""

    def close_search_form(self):
        """Cierra el formulario y limpia la búsqueda."""
        self.selected_item_id = ""
        self.selected_item_name = ""
        self.show_search_form = False
        self.reset_search()

    @rx.var(cache=False)
    def has_search_results(self) -> bool:
        """Indica si hay resultados de búsqueda."""
        return len(self.search_results) > 0

    async def set_search_text(self, value: str):
        """Actualiza el texto de búsqueda."""
        self.search_text = value
        self.error_message = ""
        await self.search_users()

    async def search_users(self):
        """Búsqueda compatible con rx.Model"""
        if not self.search_text or not self._model:
            self.search_results = []
            return

        try:
            with rx.session() as session:
                # Crear consulta con SQLModel
                statement = select(self._model).where(
                    getattr(self._model, self.search_property).ilike(f"%{self.search_text}%")
                )
                results = session.exec(statement).all()
                
                # Convertir resultados a diccionarios
                self.search_results = [{
                    "id": str(getattr(item, self.return_property)),
                    "display": str(getattr(item, self.display_property))
                } for item in results]
                
                if not self.search_results:
                    self.error_message = "No se encontraron resultados"
                    
        except Exception as e:
            self.error_message = f"Error de búsqueda: {str(e)}"
            self.search_results = []

    async def validate_input_id(self, value: str):
        """Valida el valor del input."""
        try:
            if not value:
                self.input_error = ""
                self.selected_item_id = ""
                self.selected_item_name = ""
                # Limpiar el valor en el estado padre
                parent_state = self.get_parent_state()
                if parent_state and hasattr(parent_state, self.return_property):
                    parent_state.department_id = None
                return
                
            if not self._model:
                self.input_error = "Modelo no configurado"
                return
                
            # Obtener el tipo del campo
            field = self._model.__fields__[self.return_property]
            field_type = field.type_
            
            # Si el tipo es Optional[int], extraer el tipo interno
            if hasattr(field_type, "__origin__") and field_type.__origin__ is Optional:
                field_type = field_type.__args__[0]
            
            # Convertir el valor al tipo correcto
            if field_type is int:
                converted_value = int(value)
            else:
                converted_value = value
            
            # Buscar el elemento en la base de datos
            with rx.session() as session:
                return_attr = getattr(self._model, self.return_property)
                display_attr = getattr(self._model, self.display_property)
                
                item = session.exec(
                    select(self._model).where(return_attr == converted_value)
                ).first()
                
                if item:
                    self.input_error = ""
                    self.selected_item_id = str(converted_value)
                    self.selected_item_name = str(getattr(item, self.display_property))
                    
                    # Establecer el valor en el estado padre
                    parent_state = self.get_parent_state()
                    if parent_state and hasattr(parent_state, self.return_property):
                        if field_type is int:
                            parent_state.department_id = converted_value
                        else:
                            parent_state.department_id = value
                else:
                    self.input_error = "Elemento no encontrado"
                    self.selected_item_id = ""
                    self.selected_item_name = ""
                    # Limpiar el valor en el estado padre
                    parent_state = self.get_parent_state()
                    if parent_state and hasattr(parent_state, self.return_property):
                        parent_state.department_id = None
                    
        except (ValueError, TypeError) as e:
            self.input_error = f"Valor inválido: {str(e)}"
            self.selected_item_id = ""
            self.selected_item_name = ""
            # Limpiar el valor en el estado padre
            parent_state = self.get_parent_state()
            if parent_state and hasattr(parent_state, self.return_property):
                parent_state.department_id = None
        except Exception as e:
            self.input_error = f"Error de validación: {str(e)}"
            self.selected_item_id = ""
            self.selected_item_name = ""
            # Limpiar el valor en el estado padre
            parent_state = self.get_parent_state()
            if parent_state and hasattr(parent_state, self.return_property):
                parent_state.department_id = None

    def handle_f2_key(
        self,
        code: str,
        model_name: str, 
        search_property: str,
        return_property: str,
        display_property: str
    ):
        """Manejador específico para tecla F2"""
        if code == "F2":
            self.open_search_form(
                model_name,
                search_property,
                return_property,
                display_property
            )

    def set_selected_item(self, item_id: str, item_name: str):
        """Establece el elemento seleccionado."""
        try:
            # Convertir el ID al tipo correcto según el modelo
            if self._model and hasattr(self._model, self.return_property):
                field = self._model.__fields__[self.return_property]
                field_type = field.type_
                
                # Si el tipo es Optional[int], extraer el tipo interno
                if hasattr(field_type, "__origin__") and field_type.__origin__ is Optional:
                    field_type = field_type.__args__[0]
                
                # Convertir el valor al tipo correcto
                if field_type is int:
                    converted_id = int(item_id)
                    self.input_value = str(converted_id)
                    self.selected_item_id = str(converted_id)
                    
                    # Obtener el estado padre y establecer el valor convertido
                    parent_state = self.get_parent_state()
                    if parent_state and hasattr(parent_state, self.return_property):
                        parent_state.department_id = converted_id
                else:
                    self.input_value = str(item_id)
                    self.selected_item_id = str(item_id)
                    
                    # Obtener el estado padre y establecer el valor como string
                    parent_state = self.get_parent_state()
                    if parent_state and hasattr(parent_state, self.return_property):
                        parent_state.department_id = item_id
            else:
                self.input_value = str(item_id)
                self.selected_item_id = str(item_id)
                
            self.selected_item_name = item_name
            self.show_search_form = False
            self.reset_search()
            
        except (ValueError, TypeError) as e:
            self.error_message = f"Error al convertir el valor: {str(e)}"
            self.selected_item_id = ""
            self.selected_item_name = ""
            self.input_value = ""

# ============================================================================
# Componentes
# ============================================================================

def search_input(**props) -> rx.Component:
    """Campo de búsqueda con debounce."""
    return rx.input(
        placeholder="Buscar...",
        on_change=SearchUserState.set_search_text,
        debounce=300,
        **props
    )

def item_card(item: dict) -> rx.Component:
    return rx.card(
        rx.text(item["display"], size="3", weight="bold"),
        padding="1rem",
        cursor="pointer",
        _hover={"background": "accent.2"},
        on_click=lambda: SearchUserState.set_selected_item(item["id"], item["display"]),
        width="100%"
    )

def search_results() -> rx.Component:
    """Lista de resultados de búsqueda."""
    return rx.vstack(
        rx.foreach(
            SearchUserState.search_results,
            lambda item: item_card(item=item)
        ),
        max_height="300px",
        overflow_y="auto",
        width="100%"
    )

def search_dialog(
    model_name: str = MODEL_NAME,
    search_property: str = SEARCH_PROPERTY,
    return_property: str = RETURN_PROPERTY,
    display_property: str = DISPLAY_PROPERTY,
    item_name: str = ITEM_NAME,
    width: str = WIDTH,
    **props
) -> rx.Component:
    """Diálogo de búsqueda."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.hstack(
                rx.input(
                    value=SearchUserState.input_value,
                    on_change=SearchUserState.validate_input_id,
                    on_key_down=lambda code: SearchUserState.handle_f2_key(
                        code,
                        model_name,
                        search_property,
                        return_property,
                        display_property
                    ),
                    placeholder=f"Buscar {item_name}...",
                    width=width,
                    **props
                ),
                rx.button(
                    rx.icon("search"),
                    on_click=lambda: SearchUserState.open_search_form(
                        model_name, 
                        search_property,
                        return_property,
                        display_property
                    ),
                    variant="ghost"
                ),
                rx.text(SearchUserState.selected_item_name),
                width="10%",
                align_items="center"
            )
        ),
        rx.dialog.content(
            rx.vstack(
                rx.heading(f"Buscar {item_name}", size="5"),
                rx.text(f"Busca por {search_property.replace('_', ' ')}"),
                search_input(width="100%"),
                rx.cond(
                    SearchUserState.has_search_results,
                    search_results()
                ),
                rx.cond(
                    SearchUserState.error_message != "",
                    rx.text(SearchUserState.error_message, color="red")
                ),
                rx.flex(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        on_click=SearchUserState.close_search_form
                    ),
                    spacing="3",
                    justify="end",
                    width="100%"
                ),
                spacing="4"
            ),
            style={"max_width": "500px"}
        ),
        open=SearchUserState.show_search_form
    )