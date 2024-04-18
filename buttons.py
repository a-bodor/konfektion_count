import flet as ft
from settings import BUTTON_COLOR_DEFAULT, BUTTON_COLOR_HOVER, BUTTON_COLOR_DISABLED, BUTTON_BORDER_SIZE


'''
Class for buttons
'''


# Button Without Text
class Button(ft.UserControl):
    def __init__(self, icon, tooltip, function=None):
        super().__init__()
        self.icon = icon
        self.tooltip = tooltip
        self.function = function
        self.color_default = BUTTON_COLOR_DEFAULT
        self.color_hover = BUTTON_COLOR_HOVER
        self.color_disabled = BUTTON_COLOR_DISABLED

    def build(self):
        self.button = ft.IconButton(
            icon=self.icon,
            tooltip=self.tooltip,
            style=ft.ButtonStyle(
                color={
                    ft.MaterialState.DEFAULT: self.color_default,
                    ft.MaterialState.HOVERED: self.color_hover
                },
                bgcolor={
                    ft.MaterialState.DEFAULT: self.color_hover,
                    ft.MaterialState.HOVERED: self.color_default,
                    ft.MaterialState.DISABLED: self.color_disabled

                },
                side={
                    ft.MaterialState.DEFAULT: ft.BorderSide(BUTTON_BORDER_SIZE, self.color_default),
                    ft.MaterialState.HOVERED: ft.BorderSide(
                        BUTTON_BORDER_SIZE, self.color_hover)
                }
            ),
            on_click=self.function
        )

        return self.button

    def focus(self):
        self.button.focus()
