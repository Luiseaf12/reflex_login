import reflex as rx

from auth_reflex.auth.login import require_login


@require_login
def protected_page() -> rx.Component:
    return rx.vstack(
        rx.text("Pagina protegida"),
        padding="2em",
    )
