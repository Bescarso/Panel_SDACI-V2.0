import flet as ft

from panel import *
from inventory_page import *
from login_page import *
from sdaci_page import*



def main(page: ft.Page):

    login_content = login_window(page)
    panel_content = panel_window(page)
    sdaci_content = sdaci_browser(page)
    page.add(login_content)

ft.app(target=main)
