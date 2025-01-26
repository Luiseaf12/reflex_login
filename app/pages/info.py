import reflex as rx

from ..auth.login import require_login
from ..navigation import NavState
from ..ui import index_item


@require_login
def info_page() -> rx.Component:
    return rx.vstack(
        rx.text("Informacion"),
        index_item(),
        padding="2em",
    )
