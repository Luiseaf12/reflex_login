import reflex as rx

def field_form_component(label: str, placeholder: str, name_var: str, 
                        on_change_function, type_field: str) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.text(label, font_weight="bold", mb="2"),
            rx.input(
                placeholder=placeholder,
                on_change=on_change_function,
                name=name_var,
                type_=type_field,
                required=True,
                width="100%",
                border_color="gray.200",
                _hover={"border_color": "gray.300"},
            ),
            width="100%",
        ),
        rx.box(
            rx.text(
                "Este campo es requerido",
                color="red.500",
                font_size="4",
                mt="1",
            ),
            display="none",
            _invalid={"display": "block"},
        ),
        width="100%",
        spacing="0",
        mb="4",
    )

def field_form_component_general(label: str, placeholder: str, message_validate: str, name: str,
                               on_change_function, show) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.text(label, font_weight="bold", mb="2"),
            rx.input(
                placeholder=placeholder,
                on_change=on_change_function,
                name=name,
                required=True,
                width="100%",
                border_color="gray.200",
                _hover={"border_color": "gray.300"},
            ),
            width="100%",
        ),
        rx.cond(
            show,
            rx.text(
                message_validate,
                color="red.500",
                font_size="4",
                mt="1",
            ),
        ),
        width="100%",
        spacing="0",
        mb="4",
    )
