import flet as ft


def home_windows(page: ft.Page):

    container_principal = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text('Página de inicio / Tutorial'),
                ft.Text('Hola2')
            ]
        ),
        expand=True
    )

    return container_principal


