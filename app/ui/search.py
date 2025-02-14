import reflex as rx
from sqlmodel import select, func

from ..models import (
    LocalUser,
)


class AutocompleteState(rx.State):
    """Estado para la búsqueda  con autocompletado."""

    search_text: str = ""

    @rx.var(cache=False)
    def suggestions(self) -> list[IngredientTypeModel]:
        """Obtiene una lista de elementos que coinciden con el texto de búsqueda."""
        if not self.search_text:
            return []
        search_lower = self.search_text.lower()

        # Consulta a la base de datos usando LIKE para coincidencia parcial
        with rx.session() as session:
            return session.exec(
                select(IngredientTypeModel).where(
                    func.lower(IngredientTypeModel.nombre).like(f"%{search_lower}%")
                )
            ).all()


def cell_card(IngredientType: IngredientTypeModel) -> rx.Component:

    return rx.box(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.text(IngredientType.nombre, size="2"),
                    direction="column",
                    spacing="1",
                ),
                direction="row",
                align_items="left",
                spacing="1",
            ),
            justify="between",
        )
    )


def autocomplete_search() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.input(
                rx.input.slot(
                    rx.icon(tag="search"),
                ),
                placeholder="Buscar tipos de ingredientes...",
                value=AutocompleteState.search_text,
                on_change=AutocompleteState.set_search_text,
                debounce=300,
            ),
            rx.flex(
                rx.foreach(AutocompleteState.suggestions, lambda x: cell_card(x)),
                direction="column",
                spacing="1",
            ),
            direction="column",
            spacing="1",
        ),
        style={"maxWidth": 500},
    )


def ingredient_type_search() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("search"),
            rx.text("Buscar", size="4"),
            width="100%",
            paddingX="0.5rem",
            paddingY="0.75rem",
            align="center",
            style={
                "_hover": {
                    "cursor": "pointer",
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "color": rx.color("accent", 11),
                "borderRadius": "0.5em",
            },
        ),
        on_click=autocomplete_search,
        as_="button",
        width="100%",
    )
