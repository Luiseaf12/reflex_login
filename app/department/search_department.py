import reflex as rx
from typing import List, Type, Optional
from reflex import session
from sqlmodel import select

MODEL_NAME: str = 'DepartmentModel'
SEARCH_PROPERTY: str = "nombre"
RETURN_PROPERTY: str = "id"
DISPLAY_PROPERTY: str = "nombre"
ITEM_NAME: str = "departamento"
WIDTH: str = "100%"

class SearchDepartamentState(rx.State):
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
        await self.search_departments()

    async def search_departments(self):
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
        self.input_value = value
        self.input_error = ""
        
        if not value or not self._model:
            return
            
        with rx.session() as session:
            try:
                return_attr = getattr(self._model, self.return_property)
                item = session.exec(
                    select(self._model).where(return_attr == value)
                ).first()
                
                if item:
                    self.selected_item_id = str(getattr(item, self.return_property))
                else:
                    self.input_error = "Elemento no encontrado"
                    self.selected_item_id = ""
            except Exception as e:
                self.input_error = f"Error de validación: {str(e)}"
                self.selected_item_id = ""

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
        self.selected_item_id = item_id
        self.selected_item_name = item_name
        self.input_value = item_id
        self.show_search_form = False
        self.search_text = ""
        self.search_results = []
        self.error_message = ""

# ============================================================================
# Componentes
# ============================================================================

def search_input(**props) -> rx.Component:
    """Campo de búsqueda con debounce."""
    return rx.input(
        placeholder="Buscar...",
        on_change=SearchDepartamentState.set_search_text,
        debounce=300,
        **props
    )
def item_card(item: dict) -> rx.Component:
    return rx.card(
        rx.text(item["display"], size="3", weight="bold"),
        padding="1rem",
        cursor="pointer",
        _hover={"background": "accent.2"},
        on_click=lambda: SearchDepartamentState.set_selected_item(item["id"], item["display"]),
        width="100%"
    )

def search_results() -> rx.Component:
    """Lista de resultados de búsqueda."""
    return rx.vstack(
        rx.foreach(
            SearchDepartamentState.search_results,
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
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.hstack(
                rx.input(
                    value=SearchDepartamentState.input_value,
                    on_change=SearchDepartamentState.validate_input_id,
                    on_key_down=lambda: SearchDepartamentState.handle_f2_key(
                        "F2",
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
                    on_click=lambda: SearchDepartamentState.open_search_form(
                        model_name, 
                        search_property,
                        return_property,
                        display_property
                    ),
                    variant="ghost"
                ),
                rx.text(SearchDepartamentState.selected_item_name),
                width="10%"
            )
        ),
        rx.dialog.content(
            rx.vstack(
                rx.heading(f"Buscar {item_name}", size="5"),
                rx.text(f"Busca por {search_property.replace('_', ' ')}"),
                search_input(width="100%"),
                rx.cond(
                    SearchDepartamentState.has_search_results,
                    search_results()
                ),
                rx.cond(
                    SearchDepartamentState.error_message != "",
                    rx.text(SearchDepartamentState.error_message, color="red")
                ),
                rx.flex(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        on_click=SearchDepartamentState.close_search_form
                    ),
                    spacing="3",
                    justify="end",
                    width="100%"
                ),
                spacing="4"
            ),
            style={"max_width": "500px"}
        ),
        open=SearchDepartamentState.show_search_form
    )