import flet as ft
from settings import TILE_FONT, TILE_FONT_SIZE, TILE_TITLE_SIZE, TILE_FONT_WEIGHT, TILE_TITLE_FONT_WEIGHT, TILE_ALIGNMENT, TILE_PADDING, TILE_MARGIN, TILE_COLOR, TILE_REZIZE, TILE_RADIUS, TILE_SHADOW, TILE_SPACING


'''
Class for tiles (square boxes containing information)
'''


class Tile(ft.UserControl):
    def __init__(self, content, height, title=None, padding=TILE_PADDING, border=True, transparent=False, hide_zero=False):
        super().__init__()
        self.content = content
        self.height = height
        self.title = title
        self.padding = padding
        self.shadow = TILE_SHADOW if border else False
        self.bgcolor = TILE_COLOR if not transparent else None
        self.hide_zero = hide_zero
        self.alignment = TILE_ALIGNMENT
        self.margin = TILE_MARGIN
        self.border_radius = TILE_RADIUS
        self.col = TILE_REZIZE

    def build(self):
        # Seperate Text/Nontext
        if isinstance(self.content, str):
            if self.hide_zero and self.content == '0':
                self.content = ''
            self.content = ft.Text(
                value=self.content,
                font_family=TILE_FONT,
                size=TILE_FONT_SIZE,
                weight=TILE_FONT_WEIGHT
            )
        # Title (optional)
        if self.title is None:
            self.container = self.content
        else:
            self.container = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                value=self.title,
                                font_family=TILE_FONT,
                                size=TILE_TITLE_SIZE,
                                weight=TILE_TITLE_FONT_WEIGHT
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.START
                    ),
                    ft.Row(
                        controls=[self.content],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                    ),
                ]
            )
        tile = ft.Container(
            content=self.container,
            height=self.height,
            alignment=self.alignment,
            padding=self.padding,
            margin=self.margin,
            bgcolor=self.bgcolor,
            border_radius=self.border_radius,
            shadow=self.shadow,
            col=self.col,
            expand=True
        )

        return tile

    def update_value(self, value):
        if self.page is not None:
            self.content.value = str(value)
            self.update()
