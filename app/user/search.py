import reflex as rx
from dataclasses import dataclass
from typing import List
from .state import UserState, ListState


@dataclass
class UserItem:
    """User data structure for display."""

    id: int
    username: str
    email: str
    status: str


class SearchState(rx.State):
    """State for song search functionality."""

    search_text: str = ""
    users: List[UserItem] = [
        UserItem(1, "luiseaf", "email@domain.com", "A"),
        UserItem(2, "coke", "email@domain.com", "A"),
        UserItem(3, "alvar", "email@domain.com", "A"),
    ]

    @rx.var
    def filtered_users(self) -> List[UserItem]:

        if not self.search_text:
            return self.users
        search_lower = self.search_text.lower()
        return [user for user in self.users if search_lower in user.username.lower()]


def user_card(user: UserItem) -> rx.Component:

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


def search() -> rx.Component:
    """Create the search interface.

    Returns:
        Search component with input and filtered song list.
    """
    return rx.card(
        rx.flex(
            rx.input(
                rx.input.slot(
                    rx.icon(tag="search"),
                ),
                placeholder="Buscar usuarios...",
                value=SearchState.search_text,
                on_change=SearchState.set_search_text,
                debounce=300,
            ),
            rx.flex(
                rx.foreach(SearchState.filtered_users, lambda x: user_card(x)),
                direction="column",
                spacing="1",
            ),
            direction="column",
            spacing="1",
        ),
        style={"maxWidth": 500},
    )
