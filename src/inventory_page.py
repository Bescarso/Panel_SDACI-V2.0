import flet as ft

from firebase_auth_realtimeDB import *
from firebase_database import *
from functions import *

def history(page: ft.Page):

    def get_data_fdb():
        data_list = []

        # Obtener los documentos de la colección
        docs = fdb.collection('inventory_history').stream()

        for doc in docs:
            if doc.id == "0":  # Omitir el documento con ID "0"
                continue
            
            data = doc.to_dict()
            data_list.append([
                doc.id,  # ID del documento
                data.get("equipo", "N/A"),
                data.get("fecha", "N/A"),
                data.get("justificación", "N/A"),
                data.get("cantidad", "N/A"),
                data.get("descripción", "N/A"),
            ])
        
        return data_list

    # Obtener todos los registros de Firebase
    records = get_data_fdb()
    records.sort(key=lambda x: int(x[0]))

    # Si no hay datos, mostrar mensaje en la tabla
    if not records:
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("No hay datos disponibles", italic=True), col_span=6)
                ]
            )
        ]
    else:
        # Crear las filas de la tabla con los datos de Firebase
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(record[0]))),
                    ft.DataCell(ft.Text(record[1])),
                    ft.DataCell(ft.Text(record[2])),
                    ft.DataCell(ft.Text(record[3])),
                    ft.DataCell(ft.Text(str(record[4]))),
                    ft.DataCell(ft.Text(record[5])),
                ]
            ) for record in records
        ]

    # Crear la tabla
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('N°', weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text('Equipo', weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text('Fecha', weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text('Justificación', weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text('Cantidad', weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text('Descripción', weight=ft.FontWeight.BOLD)),
        ],
        rows=rows,  # Agregar las filas generadas
        border=ft.border.all(2, "black"),
        vertical_lines=ft.BorderSide(1, "black"),
        horizontal_lines=ft.BorderSide(1, "black"),
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                # Título centrado
                ft.Container(
                    content=ft.Text(
                        "HISTORIAL DE INVENTARIO",
                        weight=ft.FontWeight.BOLD,
                        size=20,
                        text_align=ft.TextAlign.CENTER
                    ),
                    alignment=ft.alignment.center,
                    width=page.width * 0.9
                ),

                # Contenedor de la tabla de datos
                ft.Container(
                    content=ft.Column(
                        controls=[data_table],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.ALWAYS
                    ),
                    width=page.width * 0.8,
                    border=ft.border.all(1),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

def inventory(page: ft.Page):

    def edit_quantity(category: str,
                      device_name: str,
                      quantity: ft.TextField,
                      justify: ft.Dropdown,
                      description: ft.TextField,
                      dialog):

        if not validate_fields(quantity, justify, description):
            page.update()  # Actualiza la UI para mostrar los errores
            return  # Detiene la ejecución si hay errores

        actual_quantity = db.child(category).child(device_name).get().val().get('Cantidad')

        try:
            new_quantity = int(quantity.value)
            quantity_history = abs(actual_quantity - new_quantity)  # Se calcula la diferencia de cantidades
            quantity.error_text = None  # Elimina mensajes de error si ya es válido

        except ValueError:
            quantity.error_text = "Cantidad no válida. Ingrese un número."
            page.update()
            return

        update_db(category=category, device_name=device_name, new_quantity=new_quantity)

        upload_change(device_name=device_name,
                      justify=justify.value,
                      quantity=quantity_history,
                      description=description.value)
        
        for row in rows:
            if device_name in row.cells[2].content.value:
                row.cells[5] = ft.DataCell(ft.Text(str(new_quantity)))
                page.update()
                break

        page.close(dialog)


    def edit_button(e):
        selected_data = e.control.data
        device_category = selected_data['category']
        device_name = selected_data["name"]
        
        update_quantity = db.child(device_category).child(device_name).get().val().get('Cantidad')


        quantity_field = ft.TextField(
            value=str(update_quantity),
            label="Nueva cantidad",
            helper_text='Ingrese un número',
            error_text=None,
            input_filter=ft.NumbersOnlyInputFilter()
        )

        justify_field = ft.DropdownM2(
            label="Justificación",
            options=[
                ft.dropdown.Option("Ingreso"),
                ft.dropdown.Option("Retiro"),
            ],
        )

        description_field = ft.TextField(
            value=None,
            label="Descripción",
            multiline=True,
            max_lines=2,
            counter_text="{value_length} / {max_length} ",
            max_length=50,
        )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text('Editar cantidad'),
            content=ft.Text(f'Equipo: {device_name}'),
            actions=[
                quantity_field,
                justify_field,
                description_field,
                ft.ElevatedButton('Editar', on_click=lambda e: edit_quantity(device_category, device_name, quantity_field, justify_field, description_field,dialog=dialog)),
                ft.ElevatedButton('Cerrar', on_click=lambda e: page.close(dialog)),
            ],
            actions_overflow_button_spacing=15,
            #actions_alignment=ft.MainAxisAlignment.,
            
        )

        
        page.open(dialog)
        page.update()
        print("Diálogo abierto") 


    def close_dialog():
        page.close()
        page.update()


    def validate_fields(quantity: ft.TextField, justify: ft.Dropdown, description: ft.TextField) -> bool:
        """Verifica que los campos no estén vacíos y asigna mensajes de error si es necesario."""
        is_valid = True  # Variable para rastrear si todos los campos son válidos

        if not quantity.value.strip():
            quantity.error_text = "Ingrese una cantidad válida"
            is_valid = False
        else:
            quantity.error_text = None  # Elimina el mensaje de error si ya es válido

        if justify.value is None:
            justify.error_text = "Seleccione una justificación"
            is_valid = False
        else:
            justify.error_text = None

        if not description.value.strip():
            description.error_text = "Ingrese una descripción"
            is_valid = False
        else:
            description.error_text = None

        return is_valid  # Devuelve True si todos los campos son válidos, False si hay errores


    def update_info():
        devices_names_equipos, devices_properties_equipos = read_db(category='Equipos')
        devices_names_herramientas, devices_properties_herramientas = read_db(category='Herramientas')
        devices_names_insumos, devices_properties_insumos = read_db(category='Insumos')

        devices_names = devices_names_equipos + devices_names_herramientas + devices_names_insumos
        devices_properties = devices_properties_equipos + devices_properties_herramientas + devices_properties_insumos
        dictionary_category = get_category(devices_names)

        return devices_names, devices_properties, dictionary_category


    def upload_change(device_name: str,
                      justify: str,
                      quantity: int,
                      description: str):

        
        history_ref = fdb.collection('inventory_history')
        query = history_ref.order_by("correlativo").limit_to_last(1)
        results = query.get()

        for doc in results:
            last_number = int(doc.id)

        new_correlative = last_number + 1

        data_inventario = {
            "correlativo": new_correlative,
            "equipo": device_name,
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "justificación": justify,
            "cantidad": quantity,
            "descripción": description,
        }

        # Guardar en Firestore con el nuevo número correlativo como clave del documento
        fdb.collection('inventory_history').document(str(new_correlative)).set(data_inventario)

    devices_names, devices_properties, dict_cat = update_info()
    rows = []

    for i in range(len(devices_names)):
        device_name = devices_names[i]
        category = dict_cat.get(device_name, "Sin categoría")
        quantity = devices_properties[i].get('Cantidad', 'N/A')

        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(f'{i + 1}')),
                ft.DataCell(ft.Text(category)),
                ft.DataCell(ft.Text(device_name)),
                ft.DataCell(ft.Text(devices_properties[i].get('Marca', 'N/A'))),
                ft.DataCell(ft.Text(devices_properties[i].get('Modelo', 'N/A'))),
                ft.DataCell(ft.Text(quantity)),
                ft.DataCell(ft.IconButton(
                    icon=ft.Icons.EDIT,
                    on_click=edit_button,
                    data={'category': category, "name": device_name, "quantity": quantity})
                )
            ]
        )
        rows.append(row)

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('Item', weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text('Categoría', weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text('Equipo', weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text('Marca', weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text('Modelo', weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text('Cantidad', weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text(''))
        ],
        rows=rows,
        border=ft.border.all(2, "black"),
        vertical_lines=ft.BorderSide(1, "black"),
        horizontal_lines=ft.BorderSide(1, "black"),
     # Aquí puedes agregar las filas que necesites
    )

    return ft.Container(
            content=ft.Column(
                controls=[
                    # Contenedor del título centrado
                    ft.Container(
                        content=ft.Text(
                            "MATERIALES - PCI 40430", 
                            weight=ft.FontWeight.BOLD, 
                            size=20, 
                            text_align=ft.TextAlign.CENTER
                        ),
                        alignment=ft.alignment.center,
                        width=page.width  * 0.9# Asegura que ocupe todo el ancho
                    ),
                    
                    # Contenedor de la tabla de datos
                    ft.Container(
                        content=ft.Column(
                            controls=[data_table],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            scroll=ft.ScrollMode.ALWAYS
                        ),
                        border=ft.border.all(1),
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            alignment=ft.alignment.center,
            expand=True,
            #padding=5
        )

def inventory_windows(page: ft.Page):
    # Contenedor que muestra las pantallas
    container_screen = ft.Container(content=inventory(page))

    def inventory_screen(e):
        container_screen.content = inventory(page)
        page.update()

    def history_screen(e):
        view = history(page)
        container_screen.content = view
        page.update()

    # Botones con acciones definidas
    control_button = ft.TextButton('Control',
                                   width=120,
                                   icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                                   on_click=inventory_screen
                                   )

    history_button = ft.TextButton('Historial',
                                   width=120,
                                   icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                                   on_click=history_screen
                                   )

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(  # Mantiene los botones fijos en una columna
                    content=ft.Column(
                        controls=[control_button, history_button],
                        #alignment=ft.MainAxisAlignment.START
                    ),

                ),
                ft.VerticalDivider(width=5, thickness=2),
                container_screen
            ],
            expand=True
        ),
        expand=True
    )

