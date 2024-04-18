import flet as ft
from settings import SNACKBAR_TEXT_COLOR, SNACKBAR_DURATION, SNACKBAR_WIDTH


'''
Class for snackbars (information popups)
'''


class Snackbar(ft.UserControl):
    def __init__(self, text, color, icon_leading=None, icon_close=False, duration=SNACKBAR_DURATION,):
        super().__init__()
        self.text = text
        self.color = color
        self.icon_leading = icon_leading
        self.icon_close = icon_close
        self.duration = duration

    def build(self):
        snackbar = ft.SnackBar(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        self.icon_leading,
                        color=SNACKBAR_TEXT_COLOR
                    ),
                    ft.Text(
                        self.text,
                        color=SNACKBAR_TEXT_COLOR,
                        weight=ft.FontWeight.BOLD
                    )
                ]
            ),
            bgcolor=self.color,
            behavior=ft.SnackBarBehavior.FLOATING,
            show_close_icon=self.icon_close,
            duration=self.duration,
            width=SNACKBAR_WIDTH
        )

        return snackbar
