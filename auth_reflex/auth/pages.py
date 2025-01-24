import reflex as rx
from .forms import field_form_component, field_form_component_general
from .notify import notify_component
from .state import SessionState



def login_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Inicio de sesión", font_size="2xl", mb="8"),
            rx.form(
                rx.vstack(
                    field_form_component_general(
                        "Usuario",
                        "Ingrese su correo",
                        "Ingrese un correo válido",
                        "username",
                        SessionState.set_username,
                        SessionState.user_invalid
                    ),
                    field_form_component(
                        "Contraseña",
                        "Ingrese su contraseña",
                        "password",
                        SessionState.set_password,
                        "password"
                    ),
                    rx.button(
                        rx.cond(
                            SessionState.loader,
                            rx.spinner(size="3"),
                            rx.text("Iniciar sesión")
                        ),
                        type_="submit",
                        width="100%",
                        bg="blue.500",
                        color="white",
                        _hover={"bg": "blue.600"},
                        disabled=SessionState.validate_fields,
                    ),
                    width="100%",
                    spacing="4",
                ),
                as_form=True,
                on_submit=SessionState.auth_user,
                width="100%",
            ),
            rx.cond(
                SessionState.error_create_user != '',
                notify_component(SessionState.error_create_user, 'shield-alert', 'yellow'),
                rx.fragment()
            ),
            width="100%",
            max_width="400px",
            spacing="6",
            p="8",
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        bg="gray.50",
    )