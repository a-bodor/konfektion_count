import flet as ft
from settings import TILE_TITLE_SIZE, TILE_TITLE_FONT_WEIGHT, PAGE_BG_COLOR, PAGE_BG_RADIUS, PAGE_BG_PADDING, PAGE_BG_MARGIN


'''
Log Page
'''


class Log(ft.UserControl):
    def __init__(self, page, data):
        super().__init__()
        self.page = page
        self.data = data
        self.table = self.data.table_log

    def build(self):
        title = ft.Text(
            'Protokoll',
            size=TILE_TITLE_SIZE,
            weight=TILE_TITLE_FONT_WEIGHT
        )
        body = ft.Container(
            content=(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                title
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text('')
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.table
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            scroll=ft.ScrollMode.AUTO
                        )
                    ]
                )
            ),
            bgcolor=PAGE_BG_COLOR,
            border_radius=PAGE_BG_RADIUS,
            padding=PAGE_BG_PADDING,
            margin=PAGE_BG_MARGIN
        )

        return body
