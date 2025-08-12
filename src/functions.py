import flet as ft

class BarNavigation:
    def __init__(self, orientation, page):
        self.orientation = orientation
        self.page = page
        self.selected_button = ft.Ref()  # Almacena el botón seleccionado
        self.on_button_select = None  # Callback para actualizar la pantalla en otro archivo
        self.buttons = []  # Lista de botones a agregar
 
    def create_container(self, controls: list = [], alignment=None, bgcolor=None, width=None, height=None, margin=None, padding=None, spacing=None):
        widgets = controls + self.buttons
        layout_content = (
            ft.Row(controls=widgets, spacing=spacing)
            if self.orientation == 'horizontal'
            else ft.Column(controls=widgets, spacing=spacing)
        )
        return ft.Container(
            content=layout_content,
            alignment=alignment,
            bgcolor=bgcolor,
            width=width,
            height=height,
            margin=margin,
            padding=padding,
        )

    def add_buttons(self, button_texts: list):
        for button_text in button_texts:
            button = ft.TextButton(text=button_text, on_click=self.select_button)
            self.buttons.append(button)
        self.update_buttons()

    def select_button(self, e):
        self.selected_button.current = e.control.text
        self.update_buttons()
        if self.on_button_select:  
            self.on_button_select(self.selected_button.current)  # Enviar el nombre del botón seleccionado


    def update_buttons(self):
        """Actualiza el estilo de los botones en la barra de navegación."""
        for button in self.buttons:
            button.style = ft.ButtonStyle(
                bgcolor=ft.Colors.RED_300 if button.text == self.selected_button.current else ft.Colors.RED_500,
                color="white" if button.text == self.selected_button.current else "black",
                side=ft.BorderSide(width=2,color='black')
            
            )
        self.page.update()
