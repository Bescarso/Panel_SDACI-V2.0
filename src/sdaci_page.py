import flet as ft
from datetime import datetime
from firebase_auth_realtimeDB import read_db_sdaci
from firebase_database import *

#Falta configurar el boton agregar
#Falta configurar la funcion del boton borrar

def sdaci_browser (page: ft.Page):

    def handle_close(e, dialog):
        page.close(dialog)
        page.update()


    def handle_close_history(e, dialog):

        dialog_add_history.content.controls[1].value = ''
        dialog_add_history.content.controls[3].value = ''
        dialog_add_history.content.controls[4].value = ''
        page.close(dialog)
        page.update()
    

    def get_address_maintenance(e):
        address = str(address_ref.current.value.upper())
        history_data = get_maintenance_history(address)

        datatable_history_ref.current.rows.clear()
        row_index = 1

        for key, records in history_data.items():
            if key == "device_address":
                continue  # Saltar la clave que no es una colección

            for record in records:
                # Obtener la fecha y formatearla
                raw_date = record.get("date", "S/N")
                if raw_date != "S/N":
                    try:
                        if isinstance(raw_date, str):
                            date_obj = datetime.strptime(raw_date, "%d/%m/%Y")
                        else:
                            date_obj = raw_date  # ya es datetime

                        text_date = date_obj.strftime("%d/%m/%Y")
                    except Exception as ex:
                        print(f"Error en formato de fecha: {raw_date} - {ex}")
                        text_date = "Inválida"
                else:
                    text_date = "S/N"

                datatable_history_ref.current.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row_index), size=11)),
                            ft.DataCell(ft.Text(record.get("type_maintenance", "S/N"), size=11)),
                            ft.DataCell(ft.Text(text_date, size=11)),
                            ft.DataCell(ft.Text(record.get("description", "S/N"), size=11)),
                            ft.DataCell(ft.Text(record.get("action", "S/N"), size=11)),
                            ft.DataCell(ft.IconButton(
                                icon=ft.Icons.DELETE,
                                disabled=False,
                                on_click=lambda e, addr=address, history_id=record.get("id", "S/N"): open_dialog_delete(e, address=addr, idHistory=history_id)
                            ))
                        ]
                    )
                )
                row_index += 1

        page.update()


    def get_address_information(e):
        
        address = str(address_ref.current.value.upper())
        address_information = read_db_sdaci(address=address)
        address_device = get_maintenance_history(address=address)
        get_address_maintenance(address)
        
        dialog_add_history.content.controls[0].value = address


        address_confirm = address_device.get('device_address','S/N')

        # Sobrescribe el contenido del datatable_browser
        if address_confirm == address_ref.current.value and address_information is not None:
            updated_info = overwrite_datatable_browser(
                type_device=address_information.get('device', 'S/N'),
                label=address_information.get('label', 'S/N'),
                floor=address_information.get('floor', 'S/N'),
                building=address_information.get('building', 'S/N'),
                reference=address_information.get('reference', 'S/N')
            )

            datatable_browser_ref.current.rows[0].cells[1].content = ft.Container(content=updated_info[0], alignment=ft.alignment.center, width=120, height=40)
            datatable_browser_ref.current.rows[0].cells[2].content = ft.Container(content=updated_info[1], alignment=ft.alignment.center, width=200, height=40)
            datatable_browser_ref.current.rows[0].cells[3].content = ft.Container(content=updated_info[2], alignment=ft.alignment.center, width=100, height=40)
            datatable_browser_ref.current.rows[0].cells[4].content = ft.Container(content=updated_info[3], alignment=ft.alignment.center, width=100, height=40)
            datatable_browser_ref.current.rows[0].cells[5].content = ft.Container(content=updated_info[4], alignment=ft.alignment.center, width=250, height=40)
            
        else:
            page.open(error_message)
            updated_info = overwrite_datatable_browser(
                type_device='S/N',
                label='S/N',
                floor='S/N',
                building='S/N',
                reference='S/N'
            )

            datatable_browser_ref.current.rows[0].cells[1].content = ft.Container(content=updated_info[0], alignment=ft.alignment.center, width=120, height=40)
            datatable_browser_ref.current.rows[0].cells[2].content = ft.Container(content=updated_info[1], alignment=ft.alignment.center, width=200, height=40)
            datatable_browser_ref.current.rows[0].cells[3].content = ft.Container(content=updated_info[2], alignment=ft.alignment.center, width=100, height=40)
            datatable_browser_ref.current.rows[0].cells[4].content = ft.Container(content=updated_info[3], alignment=ft.alignment.center, width=100, height=40)
            datatable_browser_ref.current.rows[0].cells[5].content = ft.Container(content=updated_info[4], alignment=ft.alignment.center, width=250, height=40)
            

        page.update()


    def open_dialog_delete(e, address, idHistory):
        # Aquí puedes implementar la lógica para eliminar la información
        dialog_delete_history = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar historial"),
            content=ft.Text("¿Está seguro de que desea eliminar este historial?"),
            actions=[
                ft.TextButton("Eliminar", on_click=lambda e: confirm_delete(e, address, idHistory, dialog_delete_history)),
                ft.TextButton("Cancelar", on_click=lambda e: handle_close(e, dialog_delete_history)),
                ],
            )

        page.open(dialog_delete_history)
        page.update()


    def confirm_delete(e, address, doc_id, dialog):
        delete_data_maintenance(address=address, doc_id=doc_id)
        
        print(f"Eliminando mantenimiento de {address} con ID {doc_id}")
        get_address_information(e)
        handle_close(e, dialog=dialog)


    def upload_information (e, address_device, type_maintenance, date, description, action):

        upload_history_maintenance(address=address_device,
                                   type_maintenance=type_maintenance,
                                   date=date,
                                   description=description,
                                   action=action)

        print('Información actualizada correctamente')	
        get_address_information(e)

        handle_close_history(e,dialog_add_history)


    def date_changed (e):

        dialog_add_history.content.controls[2].value = e.control.value.strftime('%d/%m/%Y')
        page.update()
    

    def overwrite_datatable_browser(type_device, label, floor, building, reference):
        return [
            ft.Text(value=type_device, no_wrap=False, style=ft.TextStyle(size=11)),
            ft.Text(value=label, no_wrap=False, style=ft.TextStyle(size=11)),
            ft.Text(value=floor, no_wrap=True, style=ft.TextStyle(size=11)),
            ft.Text(value=building, no_wrap=True, style=ft.TextStyle(size=11)),
            ft.Text(value=reference, no_wrap=False, style=ft.TextStyle(size=11)),
        ]


    def overwrite_datatable_history(type_maintenance, date, description, action):
        return [
            ft.Text(value=type_maintenance, no_wrap=True, style=ft.TextStyle(size=11)),
            ft.Text(value=date, no_wrap=True, style=ft.TextStyle(size=11)),
            ft.Text(value=description, no_wrap=False, style=ft.TextStyle(size=11)),
            ft.Text(value=action, no_wrap=False, style=ft.TextStyle(size=11)),
        ]

    text_device = ft.Text(value='S/N', no_wrap=True, style=ft.TextStyle(size=11))
    text_label = ft.Text(value='S/N', no_wrap=False, style=ft.TextStyle(size=11))
    text_floor = ft.Text(value='S/N', no_wrap=True, style=ft.TextStyle(size=11))
    text_building = ft.Text(value='S/N', no_wrap=True, style=ft.TextStyle(size=11))
    text_reference = ft.Text(value='S/N', no_wrap=False, style=ft.TextStyle(size=11))

    information_browser = [text_device,
                           text_label,
                           text_floor,
                           text_building,
                           text_reference]
    
    address_ref = ft.Ref()
    datatable_browser_ref = ft.Ref()
    datatable_history_ref = ft.Ref()

    field_address = ft.TextField(
        value='M0-0',
        max_length=6, 
        on_submit= get_address_information,
        text_align=ft.TextAlign.CENTER,
        ref=address_ref
    )

    error_message = ft.AlertDialog(
        modal=True,
        title=ft.Text("Dirección no válida"),
        content=ft.Text("Ingrese otra dirección de dispositivo."),
        actions=[ft.TextButton("OK", on_click=lambda e: handle_close(e,dialog=error_message))]
    )

    dialog_add_history = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar historial"),
        content=ft.Column(
            controls=[
                ft.TextField(label="Dirección", value=address_ref.current.value, read_only=True),
                ft.Dropdown(label="Tipo",
                            width=250,
                            options=[
                                ft.dropdown.Option("Mant. Preventivo"),
                                ft.dropdown.Option("Mant. Correctivo"),
                                ft.dropdown.Option("Mant. de Apoyo")
                                ]),

                ft.TextField(label='Fecha',
                             value= datetime.now().strftime('%d/%m/%Y'),
                             on_click=lambda e: page.open(
                                 ft.DatePicker(
                                     first_date=datetime(year=2020, month=1, day=31),
                                     last_date=datetime(year=2026, month=12, day=31),
                                     on_change=date_changed,
                                     cancel_text='Cancelar',
                                 ),                                              
                            ),
                        ),

                ft.TextField(label="Descripción",
                             multiline=True,
                             max_lines=3,
                             counter_text = "{value_length} / {max_length}",
                             max_length=50),

                ft.TextField(label="Acción Correctiva",multiline=True,
                             max_lines=3,
                             counter_text="{value_length} / {max_length} ",
                             max_length=50),

                ft.Text(value='PRE: Trabajo programado\nCOR: Trabajo no programado\nAPO: Solicitudes de otras áreas'),
            ]
        ),
        actions=[
            ft.TextButton("Agregar", on_click=lambda e: upload_information(e=e,
                                                                           address_device=str(dialog_add_history.content.controls[0].value),
                                                                           type_maintenance=str(dialog_add_history.content.controls[1].value),
                                                                           date=datetime.strptime(dialog_add_history.content.controls[2].value, "%d/%m/%Y"),  # FECHA FORMATEADA
                                                                           description=str(dialog_add_history.content.controls[3].value),
                                                                           action=dialog_add_history.content.controls[4].value,)
            ),
            ft.TextButton("Cancelar", on_click=lambda e: handle_close_history(e, dialog=dialog_add_history)),
        ],
    )

    
    #Datatable browser

    columns_data_browser = [
        ft.DataColumn(ft.Text("DIRECCIÓN",style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("DISPOSITIVO", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("ETIQUETA", style=ft.TextStyle(size=12)),heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("EDIFICIO", style=ft.TextStyle(size=12)),heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("NIVEL", style=ft.TextStyle(size=12)),heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("REFERENCIA", style=ft.TextStyle(size=12)),heading_row_alignment=ft.MainAxisAlignment.CENTER)
    ]

    datatable_browser = ft.DataTable(
            border=ft.border.all(2, "black"),
            vertical_lines=ft.BorderSide(1, "black"),
            horizontal_lines=ft.BorderSide(1, "black"),
            heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            columns=columns_data_browser,
            ref=datatable_browser_ref,
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=field_address, alignment=ft.alignment.top_center,width=90, height=40)),
                        ft.DataCell(ft.Container(content=information_browser [0], alignment=ft.alignment.center, width=120, height=40)),
                        ft.DataCell(ft.Container(content=information_browser [1], alignment=ft.alignment.center, width=200, height=40)),
                        ft.DataCell(ft.Container(content=information_browser [2], alignment=ft.alignment.center, width=100, height=40)),
                        ft.DataCell(ft.Container(content=information_browser [3], alignment=ft.alignment.center, width=100, height=40)),
                        ft.DataCell(ft.Container(content=information_browser [4], alignment=ft.alignment.center, width=250, height=40)),
                    ],
                ),
            ],
        )
    
    #Datatable history
    columns_data_history = [
        ft.DataColumn(ft.Text("N°", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("MANTENIMIENTO", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("FECHA", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("DESCRIPCIÓN", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("ACCIÓN", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER),
        ft.DataColumn(ft.Text("BORRAR", style=ft.TextStyle(size=12)), heading_row_alignment=ft.MainAxisAlignment.CENTER)
    ]


    datatable_history = ft.DataTable(
        vertical_lines=ft.BorderSide(1, "black"),
        horizontal_lines=ft.BorderSide(1, "black"),
        heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD,),
        columns=columns_data_history,
        ref=datatable_history_ref,
        rows = [
            ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(1), size=11)),
                        ft.DataCell(ft.Text('S/N', size=11)),
                        ft.DataCell(ft.Text('S/N', size=11)),
                        ft.DataCell(ft.Text('S/N', size=11)),
                        ft.DataCell(ft.Text('S/N', size=11)),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE,
                                                  disabled=True))
                    ]
                )
        ]
    )
    
    #Containers
    container_browser = ft.Container(  
        alignment=ft.alignment.center,
        clip_behavior=ft.ClipBehavior.NONE,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[datatable_browser],
            ),
        )


    container_history = ft.Container(
        content=ft.Column(
            controls=[datatable_history],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS
            ),
        alignment=ft.alignment.top_center,
        expand=True
        )


    button_add = ft.Container(
        alignment=ft.alignment.center_right,
        width=page.width*0.8,
        content=ft.FilledButton(
        text='Agregar',
        icon=ft.Icons.ADD_OUTLINED,
        style=ft.ButtonStyle(text_style=ft.TextStyle(size=15,weight=ft.FontWeight.BOLD)),
        on_click=lambda e: page.open(dialog_add_history)
        )
    )

    #Container principal
    container_sdaci = ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                container_browser,
                button_add,
                container_history,
            ],

        ),
        
    )

    return container_sdaci