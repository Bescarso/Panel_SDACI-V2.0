import flet as ft

from functions import *

from home_page import home_windows
from inventory_page import * # Importar la función que genera la vista de inventario
from sdaci_page import sdaci_browser



def panel_window(page: ft.Page):

    def update_screen(selected_button):
        """Actualiza el contenido en función del botón seleccionado."""
        if selected_button == "Inicio":
            content_container.content = home_windows(page)
        elif selected_button == "SDACI":
            content_container.content = sdaci_browser(page)
        elif selected_button == "Inventario":
            content_container.content = inventory_windows(page)

        page.update()

    page.title = 'PANEL CONTRA INCENDIO'

    page.window.maximized = True  # Maximiza la ventana
    page.window.maximizable = True
    page.window.resizable = False

    #Mínimo alto y ancho
    page.window.min_height = 600
    page.window.min_width = 700

    # Contenedor principal para el contenido de la pantalla
    content_container = ft.Container(
        content=home_windows(page),  # Llama a la función que genera la vista de inicio
        expand=True  # Permite que se expanda al máximo
    )

    navegation_bar = BarNavigation(orientation='horizontal', page=page)
    navegation_bar.add_buttons(['Inicio','SDACI','Inventario'])
    navegation_bar.on_button_select = update_screen

    navegation_bar.selected_button.current = "Inicio"
    navegation_bar.update_buttons() 

    return ft.Container(
        content=ft.Column(
            controls=[
                navegation_bar.create_container(
                    controls=[ft.Text(value="PCI | 40430", color="white", weight=ft.FontWeight.BOLD)],
                    bgcolor='#ab2c2c',
                    padding=10
                ),
                content_container  # Contenedor del contenido, ahora expandido
            ],
            expand=True  # Asegura que ocupe toda la pantalla
        ),
        expand=True  # Asegura que este contenedor también se expanda
    )