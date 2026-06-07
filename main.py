import flet as ft
from views.index import build_page


def main(page: ft.Page):

    page.title = "Air Quality Predictor"

    build_page(page)


ft.run(main)