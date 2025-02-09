import reflex as rx

from ..auth.login import require_login
from ..navigation import NavState
from ..ui import index_item, info_item


@require_login
def protected_page() -> rx.Component:
    return rx.vstack(
        rx.text("Pagina protegida"),
        index_item(),
        info_item(),
        padding="2em",
    )
