import reflex as rx
from sqlmodel import select, func

from ..auth.model import (
    LocalUser,
)


class AutocompleteUserState(rx.State):
    """Estado para la búsqueda de usuarios con autocompletado."""

    search_text: str = ""

    @rx.var(cache=False)
    def suggestions(self) -> list[LocalUser]:
        """Obtiene una lista de usuarios que coinciden con el texto de búsqueda."""
        if not self.search_text:
            return []
        search_lower = self.search_text.lower()

        # Consulta a la base de datos usando LIKE para coincidencia parcial
        with rx.session() as session:
            return session.exec(
                select(LocalUser).where(
                    func.lower(LocalUser.username).like(f"%{search_lower}%")
                )
            ).all()


def cell_card(user: LocalUser) -> rx.Component:

    return rx.box(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.text(user.username, size="2"),
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
                placeholder="Buscar usuarios...",
                value=AutocompleteUserState.search_text,
                on_change=AutocompleteUserState.set_search_text,
                debounce=300,
            ),
            rx.flex(
                rx.foreach(AutocompleteUserState.suggestions, lambda x: cell_card(x)),
                direction="column",
                spacing="1",
            ),
            direction="column",
            spacing="1",
        ),
        style={"maxWidth": 500},
    )
