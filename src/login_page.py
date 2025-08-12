import flet as ft
import asyncio

from panel import panel_window
from inventory_page import *
from firebase_auth_realtimeDB import *

def login_window(page: ft.Page):

    async def navigate_to_docs():
        page.controls.clear()
        page.add(panel_window(page))
        page.update()

    async def login_button(e):
        try:
            confirm = login_access(email=email_ref.current.value, password=password_ref.current.value)

            if confirm:
                text_access_ref.current.value = 'Login Exitoso!'
                text_access_ref.current.color = ft.Colors.GREEN_700 
                email_ref.current.value = ''
                password_ref.current.value = ''
                page.update()
                await asyncio.sleep(2)  # Espera sin bloquear la UI
                await navigate_to_docs()
            else:
                text_access_ref.current.value = 'Email/Contraseña incorrecto.'
                text_access_ref.current.color = ft.Colors.RED_500

        except Exception as ex:
            text_access_ref.current.value = 'Error de autenticación.'
            text_access_ref.current.color = 'red'
            print(f'Error: {ex}')

        page.update()

    async def handle_keyboard(e: ft.KeyboardEvent):
        if e.key == "Enter":
            await login_button(e)

    page.title = 'Login Page'
    page.on_keyboard_event = handle_keyboard

    text_field_width = 300

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email_ref = ft.Ref()
    password_ref = ft.Ref()
    text_access_ref = ft.Ref()

    email_field = ft.TextField(
        label='Email',
        value='',
        icon=ft.Icons.ACCOUNT_CIRCLE,
        width=text_field_width,
        ref=email_ref
    )

    password_field = ft.TextField(
        label='Contraseña',
        value='',
        password=True,
        can_reveal_password=True,
        icon=ft.Icons.KEY_OUTLINED,
        width=text_field_width,
        ref=password_ref
    )

    text_access_field = ft.Text(value='',
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color='white',
                                ref=text_access_ref)

    img = ft.Image(
        src="src/assets/images/sci.jpg",
        fit=ft.ImageFit.CONTAIN,
        expand=True
    )

    login = ft.Column(
        controls=[
            ft.Text(
                spans=[ft.TextSpan(
                    text="BIENVENIDO",
                    style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, weight=ft.FontWeight.BOLD, size=30)
                )]
            ),
            ft.Text(
                spans=[ft.TextSpan(
                    text="PANEL CI - 40430",
                    style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=20)
                )]
            ),
            email_field,
            password_field,
            ft.FilledButton(text='Log in', width=100, on_click= login_button),
            text_access_field
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    # Contenedor principal con imagen y login
    container_login = ft.Container(
        ft.Row(
            controls=[
                ft.Container(img, expand=1),
                ft.Container(login, expand=1),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        expand=True,
    )

    return container_login
