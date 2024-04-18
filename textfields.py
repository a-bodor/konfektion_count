import flet as ft
from settings import TEXTFIELD_TEXT_SIZE, TEXTFIELD_WIDTH, TEXTFIELD_TEXT_ALIGNMENT, TEXTFIELD_BORDER_COLOR, COLOR_RED


'''
Class for textfields
'''


class Textfield(ft.UserControl):
    def __init__(self, value, alignment=TEXTFIELD_TEXT_ALIGNMENT, read_only=False, focus_func=None, deselect_func=None, suffix=''):
        super().__init__()
        self.value = value
        self.alignment = alignment
        self.read_only = read_only
        self.focus_func = focus_func
        self.deselect_func = deselect_func
        self.suffix = suffix

    def build(self):
        if self.value == None:
            self.value = 0
        self.textfield = ft.TextField(
            value=self.value,
            text_size=TEXTFIELD_TEXT_SIZE,
            width=TEXTFIELD_WIDTH,
            text_align=self.alignment,
            suffix=ft.Text(self.suffix),
            read_only=self.read_only,
            border_color=TEXTFIELD_BORDER_COLOR,
            focused_border_color=COLOR_RED,
            on_focus=self.focus_func,
            on_blur=self.deselect_func
        )

        return self.textfield

    def update_value(self, value):
        self.value = value
        self.controls[0].value = self.value
        self.update()
