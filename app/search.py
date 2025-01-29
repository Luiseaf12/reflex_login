import reflex as rx
from dataclasses import dataclass
from typing import List


@dataclass
class Song:
    """Song data structure."""

    title: str
    initials: str
    genre: str


class SearchState(rx.State):
    """State for song search functionality."""

    search_text: str = ""
    songs: List[Song] = [
        Song("The Less I Know", "T", "Rock"),
        Song("Breathe Deeper", "ZB", "Rock"),
        Song("Let It Happen", "TF", "Rock"),
        Song("Borderline", "ZB", "Pop"),
        Song("Lost In Yesterday", "TO", "Rock"),
        Song("Is It True", "TO", "Rock"),
    ]

    @rx.var(cache=False)
    def filtered_songs(self) -> List[Song]:

        if not self.search_text:
            return self.songs
        search_lower = self.search_text.lower()
        return [song for song in self.songs if search_lower in song.title.lower()]


def song_card(song: Song) -> rx.Component:

    return rx.box(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.text(song.title, size="2"),
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
                placeholder="Buscar canciones...",
                value=SearchState.search_text,
                on_change=SearchState.set_search_text,
                debounce=300,
            ),
            rx.flex(
                rx.foreach(SearchState.filtered_songs, lambda x: song_card(x)),
                direction="column",
                spacing="1",
            ),
            direction="column",
            spacing="1",
        ),
        style={"maxWidth": 500},
    )
