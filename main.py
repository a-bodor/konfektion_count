import flet as ft
from settings import MAIN_TITLE, THEME, WIDTH_START, HEIGHT_START, WIDTH_MIN, HEIGHT_MIN
from header import Header
from footer import Footer
from route import Route
from logic import Logic
from data import Data


'''
Main file
'''


def main(page: ft.Page):
    # Window properties
    page.title = MAIN_TITLE
    page.window_min_width = WIDTH_MIN
    page.window_min_height = HEIGHT_MIN
    page.window_width = WIDTH_START
    page.window_height = HEIGHT_START
    page.window_prevent_close = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    # page.window_maximized = True
    page.scroll = ft.ScrollMode.AUTO
    # Syling
    page.bgcolor = ft.colors.SURFACE
    page.theme_mode = 'light'
    page.theme = THEME
    # Create Objects
    data = Data(page)
    logic = Logic(page, data)
    appbar = Header(page, data, MAIN_TITLE)
    bottom_appbar = Footer(page, data, logic)
    route = Route(page, data)
    # Page
    page.appbar = appbar.build()
    page.bottom_appbar = bottom_appbar.build()
    page.floating_action_button.on_click = lambda e: logic.floating_action_btn_click(
        e)
    page.on_route_change = route.route_change
    page.on_window_event = logic.window_event

    page.update()


# Main
if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
