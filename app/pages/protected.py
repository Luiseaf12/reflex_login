import reflex as rx

from auth_reflex.auth.login import require_login
from ..navigation import NavState
from ..ui import index_item


@require_login
def protected_page() -> rx.Component:
    return rx.vstack(
        rx.text("Pagina protegida"),
        index_item(),
        padding="2em",
    )
