import reflex as rx

from ..auth.login import require_login
from ..navigation import NavState
from ..ui import index_item, protected_item


@require_login
def contact_page() -> rx.Component:
    return rx.vstack(
        rx.text("contactos"),
        index_item(),
        protected_item(),
        padding="2em",
    )
